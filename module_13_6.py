from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
import asyncio


token_api = '7928871949:AAFil2VZjlzqKZ-3OkOG7fzYfCLjUaTYdvA'
bot = Bot(token=token_api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = InlineKeyboardMarkup()
button1 = InlineKeyboardButton(text='Расчитать', callback_data='R')
button2 = InlineKeyboardButton(text='Формула', callback_data='F')
kb.add(button1)
kb.add(button2)

kb_gender = InlineKeyboardMarkup()
button_man = InlineKeyboardButton(text="Мужской", callback_data="man_gender")
button_woman = InlineKeyboardButton(text="Женский", callback_data="woman_gender")
kb_gender.add(button_man, button_woman)

kb_activity = InlineKeyboardMarkup()
button_1 = InlineKeyboardButton(text="Минимальная - 1.2", callback_data="activity_1.2")
button_2 = InlineKeyboardButton(text="Слабая - 1.375", callback_data="activity_1.375")
button_3 = InlineKeyboardButton(text="Средняя - 1.55", callback_data="activity_1.55")
button_4 = InlineKeyboardButton(text="Высокая - 1.725", callback_data="activity_1.725")
button_5 = InlineKeyboardButton(text="Экстра - 1.725", callback_data="activity_1.725")
kb_activity.add(button_1, button_2, button_3, button_4, button_5)



class UserState(StatesGroup):
    gender = State()
    activity = State()
    age = State()
    growth = State()
    weight = State()
    info = State()

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет, нажми на одну из появившихся кнопок', reply_markup=kb)

@dp.callback_query_handler(text='F')
async def info(call):
    await call.message.answer('Для мужчин:\n (10 * вес (кг) + 6.25 * рост (см) – 5 * возраст (г) + 5) * A\n'
                              'Для женщин:\n (10 * вес (кг) + 6.25 * рост (см) – 5 * возраст (г) – 161) * A')
    await call.answer()

@dp.callback_query_handler(text='R')
async def set_gender(call):
    await call.message.answer('Укажите ваш пол', reply_markup=kb_gender)
    await UserState.gender.set()

@dp.callback_query_handler(lambda c: c.data in ['man_gender', 'woman_gender'], state=UserState.gender)
async def process_gender(call, state):
    gender = 'м' if call.data == 'man_gender' else 'ж'
    await state.update_data(gender=gender)
    await call.message.answer('Какая у вас активность', reply_markup=kb_activity)
    await UserState.activity.set()

@dp.callback_query_handler(lambda c: c.data.startswith('activity_'), state=UserState.activity)
async def set_age(call, state):
    activity = float(call.data.split('_')[1])
    await state.update_data(activity=activity)
    await call.message.answer('Укажите ваш возраст')
    await UserState.age.set()
    await call.answer()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    try:
        age = int(message.text)
        if age <= 0:
            await message.answer('Пожалуйста, введите корректный возраст')
            return
    except ValueError:
        await message.answer('Пожалуйста, введите число')
        return
    await state.update_data(age=message.text)
    await message.answer('Укажите ваш рост')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    try:
        growth = float(message.text)
        if growth <= 0:
            await message.answer('Пожалуйста, введите корректный рост')
            return
    except ValueError:
        await message.answer('Пожалуйста, введите число')
        return
    await state.update_data(growth=message.text)
    await message.answer('Укажите ваш вес')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def set_calories(message, state):
    try:
        weight = float(message.text)
        if weight <= 0:
            await message.answer('Пожалуйста, введите корректный вес')
            return
    except ValueError:
        await message.answer('Пожалуйста, введите число')
        return
    await state.update_data(weight=message.text)
    data = await state.get_data()
    if data['gender'] == 'м':
        calories = ((10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) + 5) *
                    float(data['activity']))
        await message.answer(f'Ваша суточная норма каллорий: {round(calories, 2)}')
    else:
        calories = ((10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) - 161) *
                    float(data['activity']))
        await message.answer(f'Ваша суточная норма каллорий: {round(calories, 2)}')
    await state.finish()

@dp.message_handler()
async def set_info(message):
    await message.answer('Я бот помогающий твоему здоровью!'
                         'Давай рссчитаем твою суточную норму каллорий для оптимального похудения!'
                         'Расчет произведем по вормуле Миффлина-Сан Жеора!'
                         'Нажмите /start для начала расчета')

if __name__ =='__main__':
    executor.start_polling(dp, skip_updates=True)


