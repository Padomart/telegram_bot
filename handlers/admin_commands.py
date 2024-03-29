from aiogram import Router, types
from aiogram.filters import Command

from handlers.scheduler import send_scheduled_schedule
from utils.redis_conf import redis

admin_router = Router(name=__name__)


@admin_router.message(Command("show_users"))
async def show_users(message: types.Message) -> None:
    keys = await redis.keys("user_id:*")
    # Extract user IDs from the keys
    user_ids = [key.decode("utf-8").split(":")[1] for key in keys]
    if user_ids:
        await message.answer(" ".join(user_ids))
    else:
        await message.answer("Список пуст")


@admin_router.message(Command("add_user"))
async def add_new_user(message: types.Message) -> None:
    user_id = message.text.split()[-1]
    user_exists = await redis.exists(f'user_id:{user_id}')

    # If user doesn't exist, store their ID in Redis
    if not user_exists:
        await redis.set(f'user_id:{user_id}', 1)
        await message.answer(f"пользователь {user_id} зарегестрирован")
    else:
        await message.answer(f"пользователь {user_id} уже есть")


@admin_router.message(Command("delete_user"))
async def delete_user(message: types.Message) -> None:
    user_id = message.text.split()[-1]
    user_exists = await redis.exists(f"user_id:{user_id}")

    # If the user exists, delete their ID from Redis
    if user_exists:
        await redis.delete(f"user_id:{user_id}")
        print(f"id={user_id} отписался от рассылки")
        await message.answer(f"id={user_id} успешно удален")

    # Otherwise, inform the user they were not subscribed
    else:
        await message.answer(f"id={user_id} не был подписаны на рассылку.")


@admin_router.message(Command("trigger_schedule"))
async def trigger_schedule(message: types.Message) -> None:
    await send_scheduled_schedule()


@admin_router.message(Command("help"))
async def show_commands(message: types.Message):
    if message.chat.id == 1142713799:
        await message.answer("/show_users\n/add_user\n/delete_user\n/trigger_schedule")
    else:
        await message.answer("у вас нет прав")
