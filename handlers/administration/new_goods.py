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
async def add_new_tariff(message: types.Message):
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
    await AdminSteps.name.set()
    await bot.send_message(message.from_user.id, '1')
