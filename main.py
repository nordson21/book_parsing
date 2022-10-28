from bs4 import BeautifulSoup
import requests
test_url = 'https://google.com'
url = 'https://fantasy-worlds.org/lib/-genre:13/'
response = requests.get(test_url)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'lxml')
print(soup)