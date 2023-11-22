from aiogram import types
from app import dp, bot
from loader import storage
from utils.database.connection import session, Database
from states.steps import ToDelete
from .new_goods import is_admin


# Функция для получения данных всех тарифов
async def get_all_goods():
    all_goods_data = {}
    admin = session.query(Database).all()
    for goods in admin:
        all_goods_data[goods.goods_id] = goods.name
    return all_goods_data


# Функция для обновления сообщения с кнопками
# Измененная функция update_buttons
async def update_buttons(message: types.Message, start_index, goods_data):
    keyboard = types.InlineKeyboardMarkup(row_width=1)

    end_index = start_index + 5
    if end_index > len(goods_data):
        end_index = len(goods_data)

    buttons = []

    for index in range(start_index, end_index):
        keys = list(goods_data.keys())[index]
        element = goods_data[keys]
        button = types.InlineKeyboardButton(text=element, callback_data=str(keys))
        buttons.append(button)

    if start_index >= 5:
        prev_button = types.InlineKeyboardButton(text='Назад', callback_data='prev')
        buttons.append(prev_button)
    if end_index < len(goods_data):
        next_button = types.InlineKeyboardButton(text='Далее', callback_data='next')
        buttons.append(next_button)

    keyboard.add(*buttons)

    user_data = await storage.get_data(chat=message.chat.id)
    user_data['start_index'] = start_index
    await storage.set_data(chat=message.chat.id, data=user_data)

    await bot.send_message(message.chat.id, text='Какой товар вы хотите удалить?', reply_markup=keyboard)


@dp.callback_query_handler(state=ToDelete.to_delete)
async def handle_buttons(callback: types.CallbackQuery):
    user_data = await storage.get_data(chat=callback.from_user.id)
    chat_id = callback.message.chat.id
    data = callback.data

    tariffs_data = await get_all_goods()

    if data == 'prev':
        user_data = await storage.get_data(chat=chat_id)
        start_index = user_data.get('start_index', 0)
        await update_buttons(callback.message, start_index - 5, tariffs_data)
    elif data == 'next':
        user_data = await storage.get_data(chat=chat_id)
        start_index = user_data.get('start_index', 0)
        await update_buttons(callback.message, start_index + 5, tariffs_data)
    else:
        # Обработка выбранного элемента
        element_index = int(data)
        session.query(Database).filter_by(goods_id=element_index).delete()
        session.commit()
        await callback.message.edit_text(text='Товар удален')


# Обработчик команды /delete_goods
@dp.message_handler(commands=['delete_goods'], state='*')
async def delete_goods(message: types.Message):
    if is_admin(message.from_user.id):
        await ToDelete.to_delete.set()
        # Получаем данные о товарах
        goods_data = await get_all_goods()
        # Отправляем первые 5 элементов
        await update_buttons(message, 0, goods_data)
    else:
        await bot.send_message(message.from_user.id, 'У вас нет прав на эту команду.')