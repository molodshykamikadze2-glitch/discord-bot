import os
import threading
from flask import Flask
import discord
from discord.ext import tasks
from datetime import datetime, time
import pytz

# ===== Flask (фейковий сайт) =====
app = Flask(__name__)

@app.route("/")
def home():
    return "OK"  # навіть цього достатньо

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# ===== Discord bot =====
intents = discord.Intents.default()
client = discord.Client(intents=intents)

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

@client.event
async def on_ready():
    print(f"Bot logged in as {client.user}")
    send_invite.start()

@tasks.loop(minutes=1)
async def send_invite():
    kyiv = pytz.timezone("Europe/Kyiv")
    now = datetime.now(kyiv)

    if now.hour == 12 and now.minute == 0:
        channel = client.get_channel(CHANNEL_ID)
        if channel:
            invite = await channel.create_invite(
                max_uses=5,
                max_age=86400
            )
            await channel.send(f"🔗 Автоматичне запрошення:\n{invite.url}")

# ===== Запуск =====
if name == "main":
    threading.Thread(target=run_web).start()
    client.run(TOKEN)