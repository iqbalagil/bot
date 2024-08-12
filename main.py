import json
import ssl
from typing import Final
import os

import discord
from dotenv import load_dotenv
from discord import app_commands, Interaction, Intents, Message
from settings import get_response
import certifi

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_API_TOKEN')

intents: Intents = Intents.default()

CONFIG_FILE = 'config.json'


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)


config = load_config()

class BotClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        await tree.sync(guild= discord.Object(id=1011572535235711007))
        print(f'{self.user} is now running')

client = BotClient(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name='setchannel', description='Set the channel ID')
async def set_channel(interaction: Interaction, channel_id: int):
    config['channel_id'] = channel_id
    save_config(config)
    await interaction.response.send_message(f'Channel set to {channel_id}')

@tree.command(name='hello', description='Greet the bot')
async def hello(interaction: Interaction):
    await interaction.response.send_message('Hello there!')

@tree.command(name='config', description='Show current configuration')
async def config_command(interaction: Interaction):
    await interaction.response.send_message(f'Current Configuration: {json.dumps(config, indent=2)}')

@tree.command(name='message', description='Set message configuration')
async def message_command(interaction: Interaction, message: str, image_url: str, created_by: str, date_time: str):
    config['message'] = {
        'image_url': image_url,
        'text': message,
        'created_by': created_by,
        'date_time': date_time
    }
    save_config(config)
    await interaction.response.send_message(f'Message configuration set: {json.dumps(config["message"], indent=2)}')

@tree.command(name='help', description='List available commands')
async def help_command(interaction: Interaction):
    help_text = (
        "/setchannel <channel_id> - Set the channel ID\n"
        "/hello - Greet the bot\n"
        "/config - Show current configuration\n"
        "/message <message> <image_url> <created_by> <date_time> - Set message configuration\n"
    )
    await interaction.response.send_message(help_text)


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


def main() -> None:
    client.run(TOKEN)


if __name__ == '__main__':
    main()