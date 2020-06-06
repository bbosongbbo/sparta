from flask import Flask, render_template, jsonify, request #beautifulsoup에서는 requests!!
app = Flask(__name__) #flast framework를 사용하겠다!

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html') #서버에서 클라이언트로 html을 보내줌

## API 역할을 하는 부분. API란 요청을 받아서 처리하는 애!
@app.route('/test', methods=['POST'])
def test_post():
   title_receive = request.form['title_give']
   name_receive = request.form['name_give']
   print(title_receive, name_receive)
   return jsonify({'result':'success', 'msg': '이 요청은 POST!'})

@app.route('/test', methods=['GET']) #같은 경로지만 요청 type을 달리했기 때문에 두 번 사용 가능
def test_get():
   title_receive = request.args.get('title_give')
   name_receive = request.args.get('name_give')
   print(title_receive, name_receive)
   return jsonify({'result':'success', 'msg': '이 요청은 GET!'})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)