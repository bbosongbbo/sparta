from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta 

## 코딩 할 준비 ##

movie = db.movies.find_one({'title':'매트릭스'})
matrix_star = movie['star']

matrix_list = list(db.movies.find({'star':matrix_star}))

for ml in matrix_list:
    db.movies.update_one({'title':ml['title']},{'$set':{'star':0}})
    # print(ml['title'])

