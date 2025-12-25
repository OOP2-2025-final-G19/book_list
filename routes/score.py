from flask import Blueprint, render_template, request, redirect, url_for
from models import Score, User, Subject
from datetime import datetime

# Blueprintの作成 a
score_bp = Blueprint('score', __name__, url_prefix='/scores')


@score_bp.route('/')
def list():
    scores = Score.select()
    return render_template('score_list.html', title='成績一覧', items=scores)


@score_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        user_id = request.form['user_id']
        subject_id = request.form['subject_id']
        value = int(request.form['value'])
        month = int(request.form['month'])
        Score.create(user=user_id, subject=subject_id, value=value, month=month)
        return redirect(url_for('score.list'))
    
    users = User.select()
    subjects = Subject.select()
    return render_template('score_add.html', users=users, subjects=subjects)


@score_bp.route('/edit/<int:score_id>', methods=['GET', 'POST'])
def edit(score_id):
    score = Score.get_or_none(Score.id == score_id)
    if not score:
        return redirect(url_for('score.list'))

    if request.method == 'POST':
        score.user = request.form['user_id']
        score.subject = request.form['subject_id']
        score.value = int(request.form['value'])
        score.month = int(request.form['month'])
        score.save()
        return redirect(url_for('score.list'))

    users = User.select()
    subjects = Subject.select()
    return render_template('score_edit.html', users=users, subjects=subjects, score=score)

# routes/score.py 等
@score_bp.route('/graph')
def show_graph():
    from peewee import fn
    # 月別・科目別の平均点を取得
    stats = (Score
             .select(Subject.name.alias('sub_name'), Score.month, fn.AVG(Score.value).alias('avg'))
             .join(Subject)
             .group_by(Subject.name, Score.month)
             .order_by(Score.month))

    # 1月〜12月のラベルを用意
    labels = [f"{m}月" for m in range(1, 13)]
    
    # 科目ごとのデータリストを初期化
    datasets_raw = {
        "国語": [0] * 12,
        "数学": [0] * 12,
        "英語": [0] * 12
    }

    # 取得したデータを各科目のリストに振り分ける
    for s in stats:
        if s.sub_name in datasets_raw:
            datasets_raw[s.sub_name][s.month - 1] = float(s.avg)

    # テンプレートへ渡す変数を作成
    graph_data = {
        "labels": labels,
        "datasets": datasets_raw
    }

    return render_template('score_graph.html', graph_data=graph_data)
