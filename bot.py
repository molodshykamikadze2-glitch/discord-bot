import os
import asyncio
import discord
from datetime import datetime, date
import pytz

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = 1468565575658766438  # <-- СЮДИ ВСТАВ ID КАНАЛУ

intents = discord.Intents.default()
bot = discord.Client(intents=intents)

tz = pytz.timezone("Europe/Kyiv")
last_sent_date = None


@bot.event
async def on_ready():
    print(f"✅ Бот увійшов як {bot.user}")
    bot.loop.create_task(invite_scheduler())


async def invite_scheduler():
    global last_sent_date

    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)

    if channel is None:
        print("❌ Канал не знайдено. Перевір CHANNEL_ID")
        return

    while True:
        now = datetime.now(tz)

        # Якщо рівно 12:00 і ще не кидали сьогодні
        if now.hour == 12 and now.minute == 0:
            today = date.today()

            if last_sent_date != today:
                try:
                    invite = await channel.create_invite(
                        max_uses=5,
                        max_age=86400,
                        unique=True
                    )

                    await channel.send(
                        f"🔗 Автоматичне запрошення (5 використань / 1 день):\n{invite.url}"
                    )

                    last_sent_date = today
                    print("✅ Інвайт відправлено")

                except Exception as e:
                    print(f"❌ Помилка при створенні інвайта: {e}")

            # щоб не спамив у цю ж хвилину
            await asyncio.sleep(61)

        await asyncio.sleep(5)


bot.run(TOKEN)