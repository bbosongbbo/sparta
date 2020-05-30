from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

# MongoDB에서 데이터 모두 보기
all_users = list(db.users.find({},{'_id':False})) #[{내용},{내용},{내용}] #id만 빼고 가져오기

# 참고) MongoDB에서 특정 조건의 데이터 모두 보기
same_ages = list(db.users.find({'age':21}))

# john = db.users.find_one({'name':'john'},{'_id':False})
# print(john)

# 생김새
# db.people.update_many(찾을조건,{ '$set': 어떻게바꿀지 })

# 예시 - 오타가 많으니 이 줄을 복사해서 씁시다!
db.users.update_one({'name':'bobby'},{'$set':{'age':19}})

user = db.users.find_one({'name':'bobby'})
print(user)