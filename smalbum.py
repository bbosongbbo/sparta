import requests
from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
page = 0
for page in range(0, 100):
    page = page + 1
    data = requests.get('https://www.smtown.com/album?page='+str(page),headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    albums = soup.select('#content > div > div.sub_main > div > ul > li')

    for album in albums:
        title = album.select_one('a > span.title').text
        artist = album.select_one('a > span.name').text
        date = album.select_one('a > span.date').text.split('.')[0]
        year = int(date)
        if year >= 2020:
            print(title, artist, date)