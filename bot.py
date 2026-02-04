import os
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Бот увійшов як {bot.user}")

    try:
        synced = await bot.tree.sync()
        print(f"Синхронізовано {len(synced)} slash-команд")
    except Exception as e:
        print(e)

@bot.tree.command(
    name="invite",
    description="Інвайт на 5 використань і 1 день"
)
async def invite(interaction: discord.Interaction):
    invite = await interaction.channel.create_invite(
        max_uses=5,
        max_age=86400,
        unique=True
    )

    await interaction.response.send_message(
        f"🔗 Інвайт (5 використань / 1 день):\n{invite.url}"
    )

bot.run(os.getenv("DISCORD_TOKEN"))