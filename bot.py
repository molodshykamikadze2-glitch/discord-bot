import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta
import os
import pytz

TOKEN = os.getenv("DISCORD_TOKEN")  # ← тільки так
CHANNEL_ID = 1468565575658766438     # ← ID каналу

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

ua_tz = pytz.timezone("Europe/Kyiv")

async def invite_scheduler():
    await bot.wait_until_ready()

    while not bot.is_closed():
        now = datetime.now(ua_tz)

        target = now.replace(hour=12, minute=0, second=0, microsecond=0)
        if now >= target:
            target += timedelta(days=1)

        wait_seconds = (target - now).total_seconds()
        await asyncio.sleep(wait_seconds)

        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            invite = await channel.create_invite(
                max_uses=5,
                max_age=86400,
                unique=True
            )
            await channel.send(
                f"🔗 Авто-запрошення (5 використань / 1 день)\n{invite.url}"
            )

        await asyncio.sleep(86400)

@bot.event
async def on_ready():
    print(f"✅ Бот запущений як {bot.user}")
    bot.loop.create_task(invite_scheduler())

bot.run(TOKEN)