import os
import threading
from flask import Flask
import discord
from discord.ext import tasks
from datetime import datetime
import pytz

# ================= Flask (фейковий сайт) =================
app = Flask(__name__)

@app.route("/")
def home():
    return "OK"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# ================= Discord bot =================
intents = discord.Intents.default()
client = discord.Client(intents=intents)

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

KYIV_TZ = pytz.timezone("Europe/Kyiv")

@client.event
async def on_ready():
    print(f"Bot logged in as {client.user}")
    cleanup_messages.start()
    send_invite.start()

# ===== ОЧИСТКА СТАРИХ ПОВІДОМЛЕНЬ (11:55) =====
@tasks.loop(minutes=1)
async def cleanup_messages():
    now = datetime.now(KYIV_TZ)

    if now.hour == 11 and now.minute == 55:
        channel = client.get_channel(CHANNEL_ID)
        if not channel:
            return

        async for message in channel.history(limit=100):
            if message.author == client.user:
                await message.delete()

# ===== ВІДПРАВКА ІНВАЙТУ (12:00) =====
@tasks.loop(minutes=1)
async def send_invite():
    now = datetime.now(KYIV_TZ)

    if now.hour == 12 and now.minute == 0:
        channel = client.get_channel(CHANNEL_ID)
        if not channel:
            return

        invite = await channel.create_invite(
            max_uses=5,
            max_age=86400
        )

        await channel.send(
            f"🔗 Автоматичне запрошення:\n{invite.url}"
        )

# ================= ЗАПУСК =================
if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    client.run(TOKEN)