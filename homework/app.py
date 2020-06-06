from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('2nd_week.html')

# ## API 역할을 하는 부분
@app.route('/shopping', methods=['GET'])
def listing():
    #2) 주문내역보기(GET): 페이지 로딩 후 하단 주문 목록이 자동으로 보이기
    orders = list(db.orders.find({},{'_id':0}))
    return jsonify({'result':'success', 'orders': orders})

@app.route('/shopping', methods=['POST'])
def order():
    # 1) 주문하기(POST): 정보 입력 후 '주문하기' 버튼클릭 시 주문목록에 추가
    name_receive = request.form['name_give']
    quantity_receive = request.form['quantity_give']
    address_receive = request.form['address_give']
    phonenumber_receive = request.form['phonenumber_give']
    
    order = {
        'name': name_receive,
        'quantity': quantity_receive,
        'address': address_receive,
        'phonenumber': phonenumber_receive
    }
    
    return jsonify({'result': 'success', 'msg':'주문이 완료되었습니다'})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)