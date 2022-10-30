from db.models import *
from urls import url_work


def add_book_in_db(book_id, name, auth, desc, img_url, dl_url):
    book = Book.create(book_id=book_id, name=name, author=auth,
                       description=desc, image_url=img_url, download_url=dl_url)
    book.save()
    print(f'{book} added in base')


def get_last_id_from_base():
    """delete this old func"""
    return Book.select().order_by(Book.book_id.desc()).get()


def get_min_id_from_base():
    """delete this old func"""
    return Book.select().order_by(Book.book_id).get()


def del_book_from_base(book_id: int):
    """delete book from Book table by id"""
    try:
        del_book = Book.get(Book.book_id == book_id)
        del_book.delete_instance()
        print(f'Book {book_id} deleted from base')
    except Book.DoesNotExist:
        # Raise?
        print(f'Book.DoesNotExist: {book_id} not deleted!')


def get_book_from_base(book_id: int):
    """return book dict from base by id"""
    book = Book.get(Book.book_id == book_id)
    book_dict = {book.book_id: {'img_url': book.image_url, 'author': book.author,
                                'name': book.name, 'description': book.description,
                                'dload_url': book.download_url, 'book_id': book.book_id}}
    return book_dict


def set_last_sent_in_db(book_id):
    """set last sent book in LastSent table in db"""
    for book in LastSent.select():
        # delete book from LastSent table
        book.delete_instance()
        print(f'{book.book_id} deleted from last sent table')
    # add book to LastSent table
    LastSent.create(book_id=book_id)
    print(f'Book {book_id} saved in last sent table')


def get_last_sent_from_db() -> int:
    """Get last sent book id from db"""
    # Get last sent book from db
    last_book = LastSent.select()
    # Checking first start of script, if len LastSent table == 0:
    if len(last_book) == 0:
        # return min book id on first page of site, script get all books from last page on site.
        return sorted(url_work.get_books_on_page(1))[0]
    # Error check, The LastSent table must have 0 entries on first run,
    # or a maximum of 1 entry on next runs.
    elif len(last_book) > 1:
        raise DataError(f'There can only be one entry in the LastSent table.'
                        f'Records in the table LastSent {len(last_book)} ')
    # return book from LastSent table.
    return last_book[0].book_id


def clear_books_table():
    """Clear table Book in db"""
    Book.delete().where(Book.book_id != 0).execute()
    print('Table with books cleared')


def update_db():
    """Check out the latest book on the site. If it matches the last book in the database,
    then there will be no changes. If the book does not match, then the site has changed,
    the function clears the database and adds to it all the books whose id is newer than
    the last book in the database."""
    # Get last book id on site
    last_book_id = url_work.get_last_book_from_site()
    # if id == id in table LastSent in db, do nothing
    if len(LastSent.select().where(LastSent.book_id == last_book_id)) == 1:
        print('Not changes, database will not be updated')
        return None
    # else, clear Book table.
    clear_books_table()
    # get new books from site.
    new_books = url_work.get_new_books()
    # adding books to database
    for book in new_books:
        # add_book_in_db(book_id, name, auth, desc, img_url, dl_url):
        add_book_in_db(book_id=book, name=new_books[book]['name'], auth=new_books[book]['author'],
                       desc=new_books[book]['description'], img_url=new_books[book]['img_url'],
                       dl_url=new_books[book]['dload_url'])


def get_all_books_from_db():
    # crappy adding books to the list from db. Needs to be reworked.
    books_list = []
    for book_id in Book.select().order_by(Book.book_id):
        book = get_book_from_base(book_id)
        # book_id = tuple(book.keys())[0]
        # book[book_id]['book_id'] = book_id
        books_list.append(tuple(book.values())[0])
    return books_list
