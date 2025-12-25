from flask import Flask, render_template
from models import initialize_database, Score, Subject
from routes import blueprints
from collections import defaultdict
from peewee import fn
from datetime import datetime

app = Flask(__name__)

# データベースの初期化
initialize_database()

# 各Blueprintをアプリケーションに登録
for blueprint in blueprints:
    app.register_blueprint(blueprint)


@app.route('/')
def index():
    # ===== 今月取得 =====
    current_month = datetime.now().month

    # ===== ヒストグラム用（今月のみ） =====
    histograms = {}
    for subject in Subject.select():
        bins = defaultdict(int)

        for s in Score.select().where(
            (Score.subject == subject) &
            (Score.month == current_month)
        ):
            bucket = (s.value // 10) * 10
            if bucket >= 100:
                bucket = 90
            bins[bucket] += 1

        histograms[subject.name] = [bins[i] for i in range(0, 100, 10)]

    labels = [f"{i}–{i+9}" for i in range(0, 100, 10)]

    # ===== 月別平均点（折れ線グラフ） =====
    linegraphs = {}
    for subject in Subject.select():
        monthly_totals = defaultdict(int)
        monthly_counts = defaultdict(int)

        for s in Score.select().where(Score.subject == subject):
            monthly_totals[s.month] += s.value
            monthly_counts[s.month] += 1

        averages = []
        for month in range(1, 13):
            if monthly_counts[month] > 0:
                averages.append(monthly_totals[month] / monthly_counts[month])
            else:
                averages.append(0)

        linegraphs[subject.name] = {
            "labels": [f"{m}月" for m in range(1, 13)],
            "values": averages
        }

    return render_template(
        'index.html',
        labels=labels,
        histograms=histograms,
        linegraphs=linegraphs,
        current_month=current_month
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
