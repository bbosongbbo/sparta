from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome('C:\\Users\\bbosongyeon\\Desktop\\Develop\\chromedriver_win32\\chromedriver', chrome_options=options)

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

## API 역할을 하는 부분
@app.route('/itnews', methods=['POST'])
def crawling():
    
    #0. 기존 DB 날리기??
    db.itnews.drop()
    
    # 1. 클라이언트로부터 데이터를 받기
    date_receive = request.form['date_give']
    category_receive = request.form['category_give']
    date = date_receive.split('/')[2] + date_receive.split('/')[0] + date_receive.split('/')[1]

    # 2. 크롤링하기
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    url = 'https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=105&date='+str(date)+'&sid2='+str(category_receive)
   
    data = requests.get(url, headers=headers)      
    soup = BeautifulSoup(data.text, 'html.parser')

    newslist = soup.select('#main_content > div.list_body.newsflash_body > ul.type06_headline > li')
    
    for news in newslist:
        a_tag = news.select_one('dl > dt:nth-child(2) > a')
        if a_tag is not None:
            print(a_tag)
            title = a_tag.text.strip()
            articleurl = a_tag['href']

            driver.get(articleurl)

            if check_exists_by_xpath('//*[@id="main_content"]/div[1]/div[3]/div/div[3]/div[2]/div[1]/a') is True:
                driver.find_element_by_xpath('//*[@id="main_content"]/div[1]/div[3]/div/div[3]/div[2]/div[1]/a').click()
                
                try:
                    # WebDriverWait와 .until 옵션을 통해 우리가 찾고자 하는 HTML 요소를
                    # 기다려 줄 수 있습니다.
                    WebDriverWait(driver, 3).until(
                                EC.invisibility_of_element(
                                    (By.CSS_SELECTOR, "._loading")
                                )
                            )

                    html = driver.page_source # 페이지의 elements모두 가져오기
                    soup = BeautifulSoup(html, 'html.parser') # BeautifulSoup사용하기
                    summary = soup.select_one('#main_content > div.article_header > div.article_info > div > div.article_btns > div.article_btns_right > div.media_end_head_autosummary._auto_summary_wrapper > div > div.media_end_head_autosummary_layer_body > div._contents_body')
                    
                    # print(summary.text)

                    doc = {
                        'title': title,
                        'articleurl' : articleurl,
                        'summary' : summary.text,
                    }
                    # print(doc)
                    # 3. mongoDB에 데이터 넣기
                    db.itnews.insert_one(doc)
                except Exception as e:
                    print (e)
                    print("error 발생")   
        
        # photo = news.select_one('d1 > dt.photo')
        # if photo is not None:
        #     image_tag = news.select_one('dl > dt.photo > a > img')
        #     image = image_tag.get('src')
        
        #     print(image)

               

    driver.quit()    

    return jsonify({'result': 'success'})


@app.route('/itnews', methods=['GET'])
def show():
    dailynews = list(db.itnews.find({},{'_id':False}))
    return jsonify({'result':'success','all_dailynews': dailynews})

# @app.route('/itnews', methods=['GET'])
# def delete():
#     db.itnews.drop()
        
def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True
    
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)