import json
import ssl
from typing import Final
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord import Intents, Message
from discord import app_commands
from settings import get_response
import certifi

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_API_TOKEN')
print(TOKEN)

intents: Intents = Intents.default()
intents.message_content = True # NOQA

bot = commands.Bot(command_prefix='/',intents=intents, ssl=ssl.create_default_context(cafile=certifi.where()))

CONFIG_FILE = 'config.json'


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return{}


def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)


config = load_config()


@bot.command(name='setchannel')
async def set_channel(ctx, channel_id: int):
    config['channel_id'] = channel_id
    save_config(config)
    await ctx.send(f'Channel set to {channel_id}')


@bot.command(name='hello')
async def hello(ctx):
    await ctx.send('Hello there!')


@bot.command(name='config')
async def config_command(ctx):
    await ctx.send(f'Current configuration: {json.dumps(config,indent=2)}')


@bot.command(name='message')
async def message_command(ctx, message: str, image_url: str, created_by: str, date_time: str):
    config['message'] = {
        'image_url': image_url,
        'text': message,
        'created_by': created_by,
        'date_time': date_time
    }
    save_config(config)
    await ctx.send(f'Message configuration setL {json.dumps(config["message"], indent=2)}')

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print("(Message not empty because intents were enabled probably)")
        return

    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


@bot.event
async def on_ready() -> None:
        print(f'{bot.user} is now running')


# @bot.event
# async def on_message(message: Message) -> None:
#     if message.author == bot.user:
#         return
# 
#     username: str = str(message.author)
#     user_message: str = message.content
#     channel: str = str(message.channel)
# 
#     print(f'[{channel}] {username}: "{user_message}"')
#     await send_message(message, user_message)
#     await bot.process_commands(message)


def main() -> None:
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
