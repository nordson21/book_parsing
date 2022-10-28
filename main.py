from bs4 import BeautifulSoup
import requests

url = 'https://fantasy-worlds.org/lib/-genre:13/'
response = requests.get(url)
print(response)