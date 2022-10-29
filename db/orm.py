from db.models import *
from urls import url_work


def add_book_in_db(book_id, name, auth, desc, img_url, dl_url):
    book = Book.create(book_id=book_id, name=name, author=auth,
                       description=desc, image_url=img_url, download_url=dl_url)
    book.save()
    print(f'{book} added in base')


def get_last_id_from_base():
    return Book.select().order_by(Book.book_id.desc()).get()


def get_min_id_from_base():
    return Book.select().order_by(Book.book_id).get()


def del_book_from_base(book_id: int):
    try:
        del_book = Book.get(Book.book_id == book_id)
        del_book.delete_instance()
        print(f'Book {book_id} deleted from base')
    except Book.DoesNotExist:
        print(f'Book.DoesNotExist: {book_id} not deleted!')


def get_book_from_base(book_id: int):
    book = Book.get(Book.book_id == book_id)
    book_dict = {book.book_id: {'img_url': book.image_url, 'author': book.author, 'name': book.name,
                                'description': book.description, 'dload_url': book.download_url}}
    return book_dict


def set_last_sent_in_db(book_id):
    for book in LastSent.select():
        print(f'{book.book_id} deleted from last sent table')
        book.delete_instance()
    LastSent.create(book_id=book_id)
    print(f'Book {book_id} saved in last sent table')


def get_last_sent_from_db():
    last_book = LastSent.select()
    if len(last_book) != 1:
        raise DataError(f'There can only be one entry in the LastSent table.'
                        f'Records in the table LastSent {len(last_book)} ')
    return last_book[0].book_id


def clear_books_table():
    Book.delete().where(Book.book_id != 0).execute()
    print('Table with books cleared')


def update_db():
    last_book_id = url_work.get_last_book_from_site()
    if len(LastSent.select().where(LastSent.book_id == last_book_id)) == 1:
        print('Not changes, database will not be updated')
        return None
    clear_books_table()
    new_books = url_work.get_new_books()
    for book in new_books:
        # add_book_in_db(book_id, name, auth, desc, img_url, dl_url):
        add_book_in_db(book_id=book, name=new_books[book]['name'], auth=new_books[book]['author'],
                       desc=new_books[book]['description'], img_url=new_books[book]['img_url'],
                       dl_url=new_books[book]['dload_url'])


def get_all_books_from_db():
    books_list = []
    for book_id in Book.select().order_by(Book.book_id):
        book = get_book_from_base(book_id)
        book_id = tuple(book.keys())[0]
        book[book_id]['book_id'] = book_id
        books_list.append(tuple(book.values())[0])
    return books_list
