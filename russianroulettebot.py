from telethon import events
from telethon.tl.functions.messages import SetInlineBotResultsRequest
from telethon.tl.types import InputBotInlineMessageText, InputBotInlineResult
import random
import os
from telethon import TelegramClient
import logging


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)


try:
    API_ID = os.environ["APP_ID"]
    API_HASH = os.environ["APP_HASH"]
    TOKEN = os.environ["TOKEN"]
except KeyError as e:
    quit(e.args[0] + ' missing from environment variables')

bot = TelegramClient("russianroulette", API_ID, API_HASH)

bot.start(bot_token=TOKEN)

@bot.on(events.NewMessage(incoming=True, pattern="^\/start"))
async def start(event):
    await event.reply("Use me inline!")


@bot.on(events.InlineQuery)
async def roulette(event):
    builder = event.builder
    user = await bot.get_entity(event.query.user_id)
    user_name = "@" + user.username or user.first_name
    deaths = [f"{user_name}'s guts were spilled all over the floor'",
                f"{user_name} just got killed...",
                f"{user_name} just got served!",
                f"{user_name} bites the dust"]

    escapes = [f"{user_name} will live to see another day",
           f"{user_name} escaped death",
           f"{user_name} just got lucky"]

    if random.randint(1, 6) == 6:
        result = random.choice(deaths)
    else:
        result = random.choice(escapes)

    await event.answer([await builder.article("Russian Roulette", description="Pull The Trigger", text=result)])

if __name__ == "__main__":
    bot.run_until_disconnected()
