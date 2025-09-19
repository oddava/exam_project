from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from database import User

register_router = Router()

class RegisterState(StatesGroup):
    name = State()
    surname = State()
    age = State()

@register_router.message(Command("register"))
async def register_command_handler(message: Message, state: FSMContext):
    await state.set_state(RegisterState.name)

    await message.answer("Ismingiz nima?")

@register_router.message(RegisterState.name)
async def register_name_handler(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await state.set_state(RegisterState.surname)

    await message.answer("Familiyangiz ..?")

@register_router.message(RegisterState.surname)
async def register_surname_handler(message: Message, state: FSMContext):
    surname = message.text
    await state.update_data(surname=surname)
    await state.set_state(RegisterState.age)

    await message.answer("Yoshingiz nechida?")

@register_router.message(RegisterState.age)
async def register_age_handler(message: Message, state: FSMContext):
    age = message.text
    await state.update_data(age=age)

    data = await state.get_data()
    User.create(**data)
    full_info = (f"Kiritgan ma'lumotlarinigiz:\n"
                 f"Ism: {data['name']}\n"
                 f"Familiya: {data['surname']}"
                 f"Yosh: {data['age']}\n"
                 f"\nRo'yxat tugadi!")

    await message.answer(full_info)