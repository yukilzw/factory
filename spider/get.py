import requests
import pandas
from bs4 import BeautifulSoup

url = 'https://book.douban.com/latest'
headers = {
    'User-Agent': 'Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5514.400'
}
data = requests.get(url, headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

books_left = soup.find('ul', {'class': 'cover-col-4 clearfix'})
books_left = books_left.find_all('li')
books_right = soup.find('ul', {'class': 'cover-col-4 pl20 clearfix'})
books_right = books_right.find_all('li')
books = list(books_left) + list(books_right)

img_urls = []
titles = []
ratings = []
for book in books:
    img_url = book.find_all('a')[0].find('img').get('src')
    img_urls.append(img_url)

    title = book.find_all('a')[1].get_text()
    titles.append(title)

    rating = book.find('p', {'class': 'rating'}).get_text()
    rating = rating.replace('\n', '').replace(' ', '')
    ratings.append(rating)

print(img_urls)
print(titles)
print(ratings)

res = pandas.DataFrame()
res['img_urls'] = img_urls
res['titles'] = titles
res['ratings'] = ratings
res.to_csv('res.csv')