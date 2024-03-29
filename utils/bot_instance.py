from aiogram import Bot, types
from constants.constants import TOKEN
from aiogram.enums import ParseMode

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)

commands = [
    types.BotCommand(command="start", description="начало подписки"),
    types.BotCommand(command="rasp", description="расписание на сегодняшний день"),
    types.BotCommand(command="tmrw", description="расписание на завтра"),
    types.BotCommand(command="week", description="фото расписания на несколько дней"),
    types.BotCommand(command="unsubscribe", description="отписаться от рассылки расписания"),
]
