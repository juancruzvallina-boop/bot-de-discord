
import discord
import random
from discord.ext import commands
import os
import requests
from model import get_classes

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def ayuda(ctx):
    await ctx.send(f'Hola,me llamo {bot.user}! y estos son los comandos que puedes usar:\nhello\nheh\nadd\nroll\nchoose\nrepeat\njoined\nmem\nduck\ncheck\nuserinfo')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hola, soy un bot {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    for i in range(times):
        await ctx.send(content)

@bot.command()
async def joined(ctx, member: discord.Member):
    if member.joined_at is None:
        await ctx.send(f'{member} has no join date.')
    else:
        await ctx.send(f'{member} joined {discord.utils.format_dt(member.joined_at)}')

@bot.command()
async def mem(ctx):
    img_name = random.choice(os.listdir("imagenes"))
    with open(f'imagenes/{img_name}', 'rb') as f:
        print(os.listdir("imagenes"))
        picture = discord.File(f)
    await ctx.send(file=picture)

def get_duck_image_url():
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.command('duck')
async def duck(ctx):
    image_url = get_duck_image_url()
    await ctx.send(image_url)

@bot.command()
async def check(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            file_url = attachment.url
            await attachment.save(f"./{attachment.filename}")
            await ctx.send(get_classes(model_path="./keras_model.h5",labels_path="./labels.txt",image_path=f"./{file_name}"))
    else:
        await ctx.send("no subiste ninguna imagen")

# NUEVA FUNCION
@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    """Muestra información de un usuario."""
    if member is None:
        member = ctx.author

    await ctx.send(
        f'Nombre: {member.name}\n'
        f'ID: {member.id}\n'
        f'Cuenta creada: {discord.utils.format_dt(member.created_at)}\n'
        f'Se unió al servidor: {discord.utils.format_dt(member.joined_at)}'
    )

bot.run("")
