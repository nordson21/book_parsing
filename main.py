from db import orm
from aiogram.utils import executor
from aiogram import Bot, Dispatcher, types
from settings.settings import token, channel_id


bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


async def send_books_in_group():
    """Get books from db and send they in tg channel"""
    all_books_list = orm.get_all_books_from_db()
    if len(all_books_list) == 0:
        await bot.send_message(channel_id, 'There is nothing new. Cron test')
    for book in all_books_list:
        book_id = book['book_id']
        name = book["name"]
        author = book["author"]
        desc = book["description"]
        dload_url = book["dload_url"]
        min_capt_len = 64 + len(name + author + dload_url)
        full_capt_len = len(desc) + min_capt_len
        if full_capt_len > 1024:
            max_desc_len = 1024 - min_capt_len
            desc = desc[:max_desc_len]
        caption = f'Название:\n<b>{name}</b>\nАвтор:\n<b>{author}</b>\nОписание:\n<i>{desc}</i>\nКнопка:\n{dload_url}'
        await bot.send_photo(channel_id, photo=f'{book["img_url"]}', caption=caption)
        print(f'Book {book_id} sent in group.')
        orm.del_book_from_base(book_id)

if __name__ == '__main__':
    orm.update_db()
    executor.start(dp, send_books_in_group())
