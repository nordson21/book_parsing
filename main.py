from bs4 import BeautifulSoup
import requests
test_url = 'https://google.com'
url = 'https://fantasy-worlds.org/lib/-genre:13/'
response = requests.get(url)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'lxml')
all_books = soup.find_all('table', {"class": "news_body"})
