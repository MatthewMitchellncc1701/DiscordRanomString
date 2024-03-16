from typing import Final
import os
from random import randrange
from dotenv import load_dotenv
from discord import Intents, Message
from discord import app_commands
from discord.ext import commands

# Load token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# set up bot
intents: Intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


# handling startup
@bot.event
async def on_ready() -> None:
    print(f'{bot.user} is now running')
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} command(s)")
    except Exception as e:
        print(f"synced error: {e}")
    print('finished')


# main entry pint
def main() -> None:
    bot.run(token=TOKEN)


@bot.tree.command(name="ping", description='Test to see if bot is running')
async def test_running(ctx):
    await ctx.response.send_message('pong', ephemeral=True)


@bot.tree.command(name="clear", description='Complete resets the txt file')
@app_commands.checks.has_permissions(administrator=True)
async def clear_text_file(ctx):
    open('saved_strings.txt', 'w').close()
    await ctx.response.send_message(f'Filed cleared!', ephemeral=True)


@bot.tree.command(name="save", description='Save strings to save')
@app_commands.checks.has_permissions(administrator=True)
async def save_string(ctx, string: str):
    write_to_file(string)
    await ctx.response.send_message(f'String Saved!', ephemeral=True)
    get_random_line()


def write_to_file(string: str):
    f = open("saved_strings.txt", "a")
    f.write(string + '\n')
    f.close()


@bot.tree.command(name="random", description='Get a random string from the saved strings')
async def get_random(ctx):
    await ctx.response.send_message(f'{get_random_line()}')


def get_random_line():
    f = open("saved_strings.txt", "r")
    num_lines = sum(1 for _ in f)
    ran = randrange(num_lines)

    f.seek(0)
    line = f.readlines()
    rv = line[ran]

    f.close()

    return rv

if __name__ == '__main__':
    main()
