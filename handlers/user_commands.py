import datetime
import re

from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import FSInputFile
from aiogram.utils.markdown import hbold

from utils.date_utils import date_format
from utils.image_generation import generate_table_image
from utils.redis_conf import redis
from utils.web_scrapping import execute_day_schedule, scrape_schedule_table
from utils.bot_instance import bot

user_router = Router(name=__name__)


@user_router.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    user_id = message.chat.id
    user_tag = message.chat.username

    # Check if user ID already exists in Redis
    user_exists = await redis.exists(f'user_id:{user_id}')

    # If user doesn't exist, store their ID in Redis
    if not user_exists:
        await redis.set(f'user_id:{user_id}', 1)  # Use a unique key for each user
        print(f"id={user_id}(@{message.chat.username}) подписался")

    await message.answer(f"Привет, {hbold(message.from_user.full_name)}!\n"
                         f"Я бот для расписания")


@user_router.message(Command("unsubscribe"))
async def unsubscribe(message: types.Message) -> None:
    user_tag = message.chat.username
    user_id = message.chat.id

    user_exists = await redis.exists(f"user_id:@{user_id}")

    # If the user exists, delete their ID from Redis
    if user_exists:
        await redis.delete(f"user_id:@{user_id}")
        print(f"id={message.chat.id}(@{user_id}) отписался от рассылки")
        await message.answer(f"Вы успешно отписались от рассылки")

    # Otherwise, inform the user they were not subscribed
    else:
        print(f"Пользователь с ID @{user_tag}({user_id}) не найден.")
        await message.answer(f"Вы не были подписаны на рассылку.")


@user_router.message(Command("rasp"))
async def today_schedule_reply(message: types.Message = None) -> None:
    today_date = datetime.date.today().strftime("%d-%m")
    today_date = date_format(today_date)
    mess = await execute_day_schedule(today_date)
    if mess:
        for i in mess:
            await bot.send_message(chat_id=message.chat.id, text=i)
    else:
        await bot.send_message(chat_id=message.chat.id, text="Сегодня пар нет")


@user_router.message(Command("tmrw"))
async def tomorrow_schedule(message: types.Message = None) -> None:
    date = (datetime.date.today() + datetime.timedelta(1)).strftime("%d-%m")
    date = date_format(date)
    mess = await execute_day_schedule(date)
    if mess:
        for i in mess:
            await bot.send_message(chat_id=message.chat.id, text=i)
    else:
        await bot.send_message(chat_id=message.chat.id, text="Завтра пар нет")


@user_router.message(Command("week"))
async def week_schedule_image(message: types.Message) -> None:
    data = scrape_schedule_table()
    today = datetime.date.today() + datetime.timedelta(days=1)
    today_date = date_format(today.strftime("%d-%m"))
    time_delta = 7

    start_index = None
    last_index = None

    for i in data:
        if i[0].strip("-") == today_date:
            start_index = data.index(i)
            break

    for i in range(time_delta):
        last_date = date_format((today + datetime.timedelta(days=i)).strftime("%d-%m"))
        if last_date in [entry[0].strip("-") for entry in data]:
            if start_index is None:
                start_index = [i for i, entry in enumerate(data) if entry[0].strip("-") == last_date][0]
            last_index = [i for i, entry in enumerate(data) if entry[0].strip("-") == last_date][-1]

    if start_index is None or last_index is None:
        data = []

    data = data[start_index:last_index + 1]
    photo = generate_table_image(data)
    photo.save("table_image.png")
    table = FSInputFile("table_image.png")
    await message.answer_photo(table)


@user_router.message()
async def specific_day_schedule(message: types.Message) -> None:
    date_text = message.text
    date_pattern = re.compile(r'^(\d{1,2})[-/.](\d{2})$')
    match = date_pattern.match(date_text)
    if match:
        date = re.sub(r"[/.]", "-", date_text)
        date = date[1:] if date[0] == "0" else date
        mess = await execute_day_schedule(date)
        if mess:
            for i in mess:
                await message.answer(text=i)
        else:
            await message.answer(text="В этот день нет занятий")
    else:
        await message.answer("Неправильный формат даты")
