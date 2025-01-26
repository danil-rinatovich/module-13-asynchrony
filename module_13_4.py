from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio


token_api = '...'
bot = Bot(token=token_api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    gender = State()
    activity = State()
    age = State()
    growth = State()
    weight = State()
    info = State()


@dp.message_handler(text='/start')
async def set_gender(message):
    await message.answer('Укажите ваш пол (м/ж):')
    await UserState.gender.set()

@dp.message_handler(state=UserState.gender)
async def set_activity(message, state):
    if message.text.lower() not in ['м', 'ж']:
        await message.answer('Пожалуйста, введите "м" или "ж"')
        return
    await state.update_data(gender=message.text)
    await message.answer('Какая у вас активность:\n'
                         'Минимальная активность = 1.2\n'
                         'Слабая активность = 1.375\n'
                         'Средняя активность = 1.55\n'
                         'Высокая активность = 1.725\n'
                         'Экстра-активность = 1.9')
    await UserState.activity.set()

@dp.message_handler(state=UserState.activity)
async def set_age(message, state):
    try:
        activity = float(message.text)
        if activity not in [1.2, 1.375, 1.55, 1.725, 1.9]:
            await message.answer('Пожалуйста, введите корректное значение активности.')
            return
    except ValueError:
        await message.answer('Пожалуйста, введите число с точкой в качестве разделителя.')
        return
    await state.update_data(activity=message.text)
    await message.answer('Укажите ваш возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    try:
        age = int(message.text)
        if age <= 0:
            await message.answer('Пожалуйста, введите корректный возраст.')
            return
    except ValueError:
        await message.answer('Пожалуйста, введите число.')
        return
    await state.update_data(age=message.text)
    await message.answer('Укажите ваш рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    try:
        growth = float(message.text)
        if growth <= 0:
            await message.answer('Пожалуйста, введите корректный рост.')
            return
    except ValueError:
        await message.answer('Пожалуйста, введите число.')
        return
    await state.update_data(growth=message.text)
    await message.answer('Укажите ваш вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def set_calories(message, state):
    try:
        weight = float(message.text)
        if weight <= 0:
            await message.answer('Пожалуйста, введите корректный вес.')
            return
    except ValueError:
        await message.answer('Пожалуйста, введите число.')
        return
    await state.update_data(weight=message.text)
    data = await state.get_data()
    if data['gender'] == 'м':
        calories = ((10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) + 5) *
                    float(data['activity']))
        await message.answer(f'Ваша суточная норма: {round(calories, 2)}')
    else:
        calories = ((10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) - 161) *
                    float(data['activity']))
        await message.answer(f'Ваша суточная норма: {round(calories, 2)}')
    await state.finish()

@dp.message_handler()
async def set_info(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью! '
                         'Давай рссчитаем твою суточную норму каллорий для оптимального похудения! '
                         'Расчет произведем по вормуле Миффлина-Сан Жеора! '
                         'Нажмите /start для начала расчета')

if __name__ =='__main__':
    executor.start_polling(dp, skip_updates=True)

