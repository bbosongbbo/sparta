from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

import requests
from bs4 import BeautifulSoup

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

## API 역할을 하는 부분
@app.route('/itnews', methods=['POST'])
def crawling():

    # 1. 클라이언트로부터 데이터를 받기
    date_receive = request.form['date_give']
    category_receive = request.form['category_give']

    # 2. 크롤링하기
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    url = 'https://news.naver.com/main/list.nhn'
    get_params = {
        'mode':'LS2D',
        'mid':'sec',
        'sid1':'105',
        'date':date_receive,
        'sid2':category_receive,
    }
    data = requests.get(url, params = get_params, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    newslist = soup.select('#main_content > div.list_body.newsflash_body > ul.type06_headline > li')

    for news in newslist:
        title = news.select-one('dl > dt:nth-child(2) > a').text
        image = news.select-one('dl > dt.photo > a')
        # 3줄요약은 아직 모르겠다

        dailynews = {
            'title': title,
            'image': image,
            #'3줄요약': 3줄요약
        }

    # 3. mongoDB에 데이터 넣기
    db.itnews.insert_one(dailynews)

    return jsonify({'result': 'success'})



@app.route('/itnews', methods=['GET'])
def show():
    return jsonify({'result':'success', 'msg': '이 요청은 GET!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)