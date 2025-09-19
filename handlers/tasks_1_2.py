from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.filters import CommandStart
from aiogram.types import Message

t12_router = Router()


@t12_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Assalomu alaylum!")


@t12_router.message(F.content_type.in_(ContentType.PHOTO))
async def photo_handler(message: Message) -> None:
    await message.answer("Rasm qabul qilindi!")


@t12_router.message(F.content_type.in_(ContentType.DOCUMENT))
async def photo_handler(message: Message) -> None:
    await message.answer("Fayl saqlandi!")


@t12_router.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")