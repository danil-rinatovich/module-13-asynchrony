from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio


token_api = ''
bot = Bot(token=token_api)
dispatcher = Dispatcher(bot, storage=MemoryStorage())


@dispatcher.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')

@dispatcher.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ =='__main__':
    executor.start_polling(dispatcher, skip_updates=True)