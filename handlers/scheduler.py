import datetime

from aiogram import exceptions
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from utils.bot_instance import bot
from utils.date_utils import date_format
from utils.redis_conf import redis
from utils.web_scrapping import execute_day_schedule

scheduler = AsyncIOScheduler()


@scheduler.scheduled_job('cron', hour=12, minute=00, timezone='Europe/Moscow')
async def send_scheduled_schedule():
    await today_schedule_notification()


async def today_schedule_notification() -> None:
    keys = await redis.keys("user_id:*")
    # Extract user IDs from the keys
    user_ids = [key.decode("utf-8").split(":")[1] for key in keys]
    today_date = datetime.date.today().strftime("%d-%m")
    today_date = date_format(today_date)
    mess = await execute_day_schedule(today_date)
    if user_ids and mess:
        for user in user_ids:
            try:
                for i in mess:
                    await bot.send_message(chat_id=user, text=i)
            except exceptions.TelegramForbiddenError:
                continue
