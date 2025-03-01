from aiogram import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

aip='dkfdkjfhdkjfhdjlhkjkjhkhjkjh749875'#Ромдомные токены, не используйте их в реальной работе
bot=Bot(token=aip)
b=Dispatcher(bot,storage= MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@b.message_handler(text=['start','/start'])
async def start(message):
    print(f'Мы получили собщение {message.text} ')
    await message.answer( f'Привет! Я бот помогающий твоему здоровью.\n Для начала прохождения теста введите /Calories ')

@b.message_handler(text=['Calories','/Calories'])
async def set_age(message):
        await message.answer('Введите ваш возраст:')
        print(f'мы сохранили {message.text}')
        await UserState.age.set()


@b.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=int(message.text))
    await message.answer('Введите ваш рост:')
    print(f'мы сохранили {message.text}')
    await UserState.growth.set()


@b.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=float(message.text))
    await message.answer('Введите ваш вес:')
    print(f'мы сохранили {message.text}')
    await UserState.weight.set()



@b.message_handler(state=UserState.weight)
async def send_calories(message,state):
    await state.update_data(weight=float(message.text))
    data= await state.get_data()
    # Simplified Mifflin - St Jeor formula for calorie calculation (example for women)
    calories = 655 + (9.6 * data['weight']) + (1.8 * data['growth']) - (4.7 * data['age'])
    await message.answer(f'Ваша максимальная норма калорий: {calories}')
    await state.finish()




if __name__ == '__main__':
    executor.start_polling(b, skip_updates=True)