from flask import Blueprint, render_template, request, redirect, url_for, jsonify, abort
from models import Registration
from datetime import datetime
from peewee import *
import base64 # Base64を画像に戻すよう
import os # フォルダ作成・パス操作用
import uuid # 重複防止

# Blueprintの作成
registration_bp = Blueprint('registration', __name__, url_prefix='/books')

@registration_bp.route('/')
def list():
    books = Registration.select()
    return render_template('registration_list.html', title='書籍一覧(テスト用)', items=books)
    # URLでhttp://localhost:8080/books/と入力することでデータ登録ができているのか確認することができる

@registration_bp.route('/add', methods=['GET', 'POST'])
def add():
    
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        day_str = request.form['day']
        day = datetime.strptime(day_str, '%Y-%m-%d').date()
        # datetime.strptime(day_str, '%Y/%m/%d').date()
        # pythonのdatetimeクラスのstrptimeを使用することで文字列を日付にしている
        #.date()とすることで日付のみ取り出す
        review = request.form['review']
        thoughts = request.form['thoughts']
        is_read = bool(request.form.get('is_read')) 
        #bool(request.form.get('is_read')とすることでチェックボックスにチェックがない時はfalseとして扱える
        #request.form.get('is_read')はgetにすることで任意になり、()になるのは関数呼び出しであるため

        image_data=request.form.get('image_data')
        image_path=None
        if image_data:
            try:
                header, encoded = image_data.split(",", 1)#base64を,で分割している
                binary = base64.b64decode(encoded)#再変換を行う
                # 保存先ディレクトリ
                save_dir = "static/uploads"#
                os.makedirs(save_dir, exist_ok=True)#
                # ファイル名生成
                filename = f"{uuid.uuid4()}.png"
                image_path = f"{save_dir}/{filename}"
                # ファイル保存
                with open(image_path, "wb") as f:
                    f.write(binary)
            except Exception as e:
                print("画像保存エラー:", e)
                image_path = None



        Registration.create(
            title=title,
            author=author,
            day=day,
            review=review,
            thoughts=thoughts,
            is_read=is_read,
            image_path=image_path
        )#行の追加
        return redirect(url_for('registration.add'))
        # submit後index.htmlに戻る
    
    return render_template('registration_add.html')

@registration_bp.route('/read')
def read_list():
    sort = request.args.get('sort', 'day')  # ソート項目を入れる変数(デフォルトは登録日)
    order = request.args.get('order', 'desc') # 昇順降順を入れる変数(デフォルトは降順)
    keyword = request.args.get('q', '').strip() # 検索ワードを入れる

    # ソート対象の対応表（安全対策）
    sort_columns = {
        'title': Registration.title,
        'author': Registration.author,
        'day': Registration.day,
        'review': Registration.review,
    }

    # is_read変数がtrueのもの(読了済みであるもの)のみを抽出する
    query = Registration.select().where(Registration.is_read == True)

    # 検索条件追加
    if keyword:
        query = query.where(Registration.title.contains(keyword))

    if sort in sort_columns:
        if order == 'asc':
            query = query.order_by(sort_columns[sort].asc())
        else:
            query = query.order_by(sort_columns[sort].desc())

    return render_template(
        'registration_read_list.html',
        items=query,
        sort=sort,
        order=order,
        keyword=keyword
    )

@registration_bp.route('/unread')
def unread_list():
    sort = request.args.get('sort', 'day')
    order = request.args.get('order', 'desc')
    keyword = request.args.get('q', '').strip()

    sort_columns = {
        'title': Registration.title,
        'author': Registration.author,
        'day': Registration.day,
        'review': Registration.review,
    }

    query = Registration.select().where(Registration.is_read == False)

    if keyword:
        query = query.where(Registration.title.contains(keyword))

    if sort in sort_columns:
        if order == 'asc':
            query = query.order_by(sort_columns[sort].asc())
        else:
            query = query.order_by(sort_columns[sort].desc())

    return render_template(
        'registration_unread_list.html',
        items=query,
        sort=sort,
        order=order,
        keyword=keyword
    )

@registration_bp.route('/graphs')
def graphs():
    # --- A. 折れ線グラフ用データ作成（月別・読了/未読別） ---
    
    # 基本のクエリ定義
    base_query = Registration.select()
    selected_year = request.args.get('year', 'all')

    # 年が選択されている場合、その年でフィルタリング（WHERE句を追加）
    if selected_year and selected_year != 'all':
        base_query = base_query.where(fn.strftime('%Y', Registration.day) == selected_year)

    # 登録日(day)から「年-月」を取り出して集計
    query = (Registration
             .select(fn.strftime('%Y-%m', Registration.day).alias('month'), 
                     Registration.is_read,
                     fn.COUNT(Registration.id).alias('count'))
             .group_by(fn.strftime('%Y-%m', Registration.day), Registration.is_read)
             .order_by(fn.strftime('%Y-%m', Registration.day)))

    # 集計結果を辞書に整理
    temp_data = {} 
    
    for item in query:
        m = item.month
        if not m: continue # 日付がないデータはスキップ

        if m not in temp_data:
            temp_data[m] = {'read': 0, 'unread': 0}
            
        if item.is_read:
            temp_data[m]['read'] = item.count
        else:
            temp_data[m]['unread'] = item.count

    # グラフのX軸（月）を作成
    all_months = sorted(temp_data.keys())

    # Chart.jsに渡すデータリストを作成
    read_values = [temp_data[m]['read'] for m in all_months]
    unread_values = [temp_data[m]['unread'] for m in all_months]

    # テンプレートへ渡すデータ
    linegraphs_data = {
        '読了': {
            'labels': all_months,
            'values': read_values
        },
        '未読': {
            'labels': all_months,
            'values': unread_values
        }
    }

    # --- B. ヒストグラム用データ（評価1〜5の分布） ---
    
    # 評価(review)ごとに集計
    review_query = (Registration
                    .select(Registration.review, fn.COUNT(Registration.id).alias('count'))
                    .where(Registration.review.is_null(False)) 
                    .group_by(Registration.review))
    
    # ★1〜★5 のカウントを初期化
    hist_counts = [0, 0, 0, 0, 0]

    for item in review_query:
        try:
            r_val = int(item.review)
            if 1 <= r_val <= 5:
                hist_counts[r_val - 1] = item.count
        except (ValueError, TypeError):
            continue

    histograms_data = {
        '全期間の評価分布': hist_counts
    }
    
    hist_labels = ['★1', '★2', '★3', '★4', '★5']

    # 画面を表示
    return render_template('graph_page.html',
                           linegraphs=linegraphs_data,
                           histograms=histograms_data,
                           labels=hist_labels)

@registration_bp.route('/update/<int:id>', methods=['POST'])
def update(id):
    book = Registration.get_by_id(id)
    data = request.get_json()

    field = data.get('field')
    value = data.get('value')

    # 空欄チェック（共通）
    if value is None or str(value).strip() == "":
        abort(400, "空欄は許可されていません")

    # 評価チェック
    if field == 'review':
        try:
            value = int(value)
        except ValueError:
            abort(400)

        if not (0 <= value <= 5):
            abort(400, "評価は0〜5")

    setattr(book, field, value)
    book.save()

    return jsonify({'status': 'ok'})

