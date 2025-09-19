from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

menu_router = Router()

@menu_router.message(Command("menu"))
async def menu_handler(message: Message):
    ikb = InlineKeyboardBuilder()
    ikb.row(
        InlineKeyboardButton(text="🍕 Pizza", callback_data="btn_Pizza"),
        InlineKeyboardButton(text="🥤 Cola", callback_data="btn_Cola")
    )
    ikb.row(
        InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel")
    )

    await message.answer("Menu", reply_markup=ikb.as_markup())

@menu_router.callback_query(F.data.startswith("btn_"))
async def menu_callback_handler(query: CallbackQuery):
    await query.message.delete()
    name = query.data.split("_")[1]
    await query.message.answer(f"Size {name} tanladingiz")

@menu_router.callback_query(F.data == "cancel")
async def menu_cancel_callback_handler(query: CallbackQuery):
    await query.message.delete()
    await query.message.answer("Menyu yopildi")