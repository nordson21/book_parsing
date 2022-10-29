from bs4 import BeautifulSoup
import requests
from db import orm


def get_books_on_page(page_num: int):
    url_prefix = 'https://fantasy-worlds.org'
    url = f'https://fantasy-worlds.org/lib/-genre:13/page{page_num}'
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    all_books = soup.find_all('table', {"class": "news_body"})
    books_on_page = {}
    for b in all_books:
        image_inner_url = b.find('img')['src']
        image_url = url_prefix + image_inner_url
        book_id = int(image_inner_url.split('/')[-1].split('.')[0])
        author = b.find('a', {'itemprop': 'author'}).text
        name = b.find('span', {'itemprop': 'name'}).text
        description = b.find('span', {'itemprop': 'description'}).text
        description = description.replace("\r\n", "")
        dload_book_inner_url = b.find('a', {'data-nb': 'button'})['href']
        download_url = url_prefix + dload_book_inner_url
        books_on_page[book_id] = {'img_url': image_url, 'author': author, 'name': name, 'description': description,
                                  'dload_url': download_url}
    return books_on_page


def get_new_books(num_of_pages=5):
    new_books = {}
    last_book_id = orm.get_last_sent_from_db()
    print(f'last book in base: {last_book_id}')
    for num in range(1, num_of_pages + 1):
        books_on_page = get_books_on_page(num)
        new_books = new_books | books_on_page
        if last_book_id in books_on_page:
            del_list = []
            for book_id in new_books:
                if book_id <= last_book_id:
                    del_list.append(book_id)
            for book_id in del_list:
                del new_books[book_id]
            new_last_book_id = sorted(list(new_books.keys()))[-1]
            orm.set_last_sent_in_db(new_last_book_id)
            return new_books
        elif num == num_of_pages:
            raise IndexError(f'last book_id {last_book_id} not found on last {num_of_pages} pages')


def get_last_book_from_site():
    last_book = sorted(get_books_on_page(1))[-1]
    return last_book
