from aiogram import types
from app import bot, dp
#from states.steps import Steps
from utils.database.connection import Database, session


@dp.message_handler(commands='start', state='*')
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Привіт, {}!👋\n'.format(message.from_user.first_name))

