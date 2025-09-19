from aiogram import Router

from middlewares import LoggingMiddleware
from .register import register_router
from .tasks_1_2 import t12_router

from .menu import menu_router

router = Router()
router.message.middleware(LoggingMiddleware())
router.include_router(register_router)
router.include_router(menu_router)
router.include_router(t12_router)
