import asyncio
import logging
import sys

from aiogram import Dispatcher

from handlers.admin_commands import admin_router
from handlers.scheduler import scheduler
from handlers.user_commands import user_router
from utils.bot_instance import bot, commands


def register_router(dp: Dispatcher) -> None:
    dp.include_router(admin_router)
    dp.include_router(user_router)


async def main() -> None:
    dp = Dispatcher()
    register_router(dp)
    scheduler.start()
    await bot.set_my_commands(commands)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
