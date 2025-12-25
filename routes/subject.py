from flask import Blueprint, render_template, request, redirect, url_for
from models import Subject

# Blueprintの作成
subject_bp = Blueprint('subject', __name__, url_prefix='/subjects')


@subject_bp.route('/')
def list():
    subjects = Subject.select()
    return render_template('subject_list.html', title='科目一覧', items=subjects)


@subject_bp.route('/add', methods=['GET', 'POST'])
def add():
    
    # POSTで送られてきたデータは登録
    if request.method == 'POST':
        name = request.form['name']
        Subject.create(name=name)
        return redirect(url_for('subject.list'))
    
    return render_template('subject_add.html')


@subject_bp.route('/edit/<int:subject_id>', methods=['GET', 'POST'])
def edit(subject_id):
    subject = Subject.get_or_none(Subject.id == subject_id)
    if not subject:
        return redirect(url_for('subject.list'))

    if request.method == 'POST':
        subject.name = request.form['name']
        subject.save()
        return redirect(url_for('subject.list'))

    return render_template('subject_edit.html', subject=subject)