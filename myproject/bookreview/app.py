from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

## API 역할을 하는 부분
@app.route('/reviews', methods=['POST'])
def write_review():
    # 1. 클라이언트가 준 title, author, review 가져오기
    # 1-1. title 가져오기
    title_receive = request.form['title_give']
    # 1-2. author 가져오기
    author_receive = request.form['author_give']
    # 1-3. review 가져오기
    review_receive = request.form['review_give']
    # 2. DB에 정보 삽입하기
    # 2-1. 삽입할 dict 만들기
    doc = {
        'title':title_receive,
        'author':author_receive,
        'review':review_receive
    }
    # 2-2. DB에 삽입하기
    db.bookreview.insert_one(doc)
    # 3. 성공 여부 & 성공 메시지 반환하기
    return jsonify({'result':'success', 'msg': '저장이 완료되었습니다'})

@app.route('/reviews', methods=['GET'])
def read_reviews():
    # 1. DB에서 리뷰 정보 모두 가져오기
    reviews = list(db.bookreview.find({},{'_id':False}))
    # 2. 성공 여부 & 리뷰 목록 반환하기
    return jsonify({'result':'success', 'all_review': reviews})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)