from io import BytesIO
from PIL import Image
from aiogram import types
from app import dp, bot
from loader import storage
from utils.database.connection import session, Database
from data import config
from utils.misc.commands import set_admin_commands
from states.steps import AdminSteps
import re
import validators


# Функция для проверки админов
def is_admin(user_id):
    return str(user_id) in config.ADMINS.split(',')


@dp.message_handler(commands=['admin'], state='*')
async def start_admin_panel(message: types.Message):
    if is_admin(message.from_user.id):
        await bot.send_message(message.from_user.id, 'Вітаю, пане Адмін')
        await set_admin_commands(dp)
    else:
        await bot.send_message(message.from_user.id, 'У вас немає прав на цю команду.')


@dp.message_handler(commands=['new_goods'], state='*')
async def add_new_goods(message: types.Message):
    if is_admin(message.from_user.id):
        session.query(Database).filter_by(user_id=message.chat.id).delete()
        existing_user = session.query(Database).filter_by(user_id=message.chat.id).first()
        if existing_user:
            pass
        else:
            # Додати новий запис про користувача в базу даних
            new_user = Database(user_id=message.chat.id)
            session.add(new_user)
            session.commit()
        await bot.send_message(message.chat.id, 'Введіть назву товару:')
        await AdminSteps.name.set()
    else:
        await bot.send_message(message.from_user.id, 'У вас немає прав на цю команду.')


@dp.message_handler(state=AdminSteps.name)
async def name_to_add(message: types.Message):
    admin = session.query(Database).filter_by(user_id=message.chat.id).first()
    admin.name = message.text
    session.commit()
    await bot.send_message(message.from_user.id, 'Яка кількість є в наявності?(шт)')
    await AdminSteps.quantity.set()


@dp.message_handler(state=AdminSteps.quantity)
async def quantity_to_good(message: types.Message):
    admin = session.query(Database).filter_by(user_id=message.chat.id).first()
    admin.quantity = message.text
    session.commit()
    await bot.send_message(message.from_user.id, 'Яка ціна за штуку?(грн)')
    await AdminSteps.price.set()


@dp.message_handler(state=AdminSteps.price)
async def price_to_good(message: types.Message):
    admin = session.query(Database).filter_by(user_id=message.chat.id).first()
    admin.price = int(message.text)
    session.commit()
    await bot.send_message(message.chat.id, "Додайте фото товару:")
    await AdminSteps.photo.set()


@dp.message_handler(content_types=['photo', 'text'], state=AdminSteps.photo)
async def photo_to_add(message: types.Message):
    try:
        if message.text:
            await bot.send_message(message.from_user.id, 'Додайте фото')
        elif message.photo:
            admin = session.query(Database).filter_by(user_id=message.chat.id).first()
            photo = message.photo[-1]
            file = await photo.get_file()

            # Преобразование изображения в байты
            image_bytes = BytesIO()
            await file.download(destination_file=image_bytes)
            image_bytes.seek(0)

            # Открытие изображения с использованием Pillow
            image = Image.open(image_bytes)

            # Преобразование изображения обратно в байты
            image_bytes = BytesIO()
            image.save(image_bytes, format='JPEG')
            image_bytes.seek(0)

            admin.photo = image_bytes.read()
            admin.user_id = None
            session.commit()
            await bot.send_message(message.from_user.id, 'Товар успішно додано')
            await dp.current_state().reset_state()
    except Exception as error:
        print(error)
        await bot.send_message(message.chat.id, 'Виникла помилка')

