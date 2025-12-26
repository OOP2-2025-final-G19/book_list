from flask import Blueprint, render_template, request, redirect, url_for
from models import Registration
from datetime import datetime
from peewee import *

# Blueprintの作成
registration_bp = Blueprint('registration', __name__, url_prefix='/books')

@registration_bp.route('/')
def list():
    books = Registration.select()
    return render_template('registration_list.html', title='書籍一覧(テスト用)', items=books)
    # URLでhttps://localhost:8080/books/と入力することでデータ登録ができているのか確認することができる


@registration_bp.route('/add', methods=['GET', 'POST'])
def add():
    
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        day = request.form['day']
        review = request.form['review']
        thoughts = request.form['thoughts']
        is_read = bool(request.form.get('is_read')) 
        #bool(request.form.get('is_read')とすることでチェックボックスにチェックがない時はfalseとして扱える
        #request.form.get('is_read')はgetにすることで任意になり、()になるのは関数呼び出しであるため

        Registration.create(
            title=title,
            author=author,
            day=day,
            review=review,
            thoughts=thoughts,
            is_read=is_read
        ) #行の追加
        return redirect(url_for('registration.add'))
        # submit後index.htmlに戻る
    
    return render_template('registration_add.html')