from aiogram import executor
from loader import dp, bot
from utils.misc.admins_notify import on_startup_notify
import handlers

#from utils.misc.commands import set_default_commands


async def on_startup(dispatcher):
    #await set_default_commands(dispatcher)
    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
