import re
import os
import time
import discord
from discord.ext import commands

from projects import jojofansmeetup, ffroll

from multiprocessing.pool import ThreadPool
from selenium.webdriver.chrome.options import Options

token = os.environ.get('bot_token')

opts = Options()
opts.headless = True

jojo_terms = re.compile(r'anime|pirate|bizarre|loomian|demon|fruits|ro-ghoul|slayer|jojo|stands|universal|dragon'
                        r'|piece|beyond|ultimate|extraordinary|day|universe|fairy|project|year|shinobi|rogue|lineage'
                        r'|ken|omega|titan|elemental|deadly|slayers|hunter|hxh|jjba|ordinary|fairy|tail|saitama'
                        r'|naruto|ninja|magic|aot|academia|mha|sharingan|modded|haikyuu|online|sakura|bleach|ghoul'
                        r'|tokyo|flame', re.IGNORECASE)

pool = ThreadPool(processes=1)

client = discord.Client()
client2 = commands.Bot(command_prefix='?')

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client2.command()
async def user(ctx, args):
    await ctx.send(str(client2.get_user(args)))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '?jojo':
        async_result = pool.apply_async(jojofansmeetup.trayJojo)
        return_value = async_result.get()

        if jojo_terms.findall(return_value):  # truthy if 0<
            response = f"jojo fans meetup tray is playing {return_value}"
        else:
            response = f'no jojos meetup :( tray is playing {return_value}'

        await message.channel.send(response)

    elif message.content.endswith('?'):
        await message.add_reaction('👍')
        await message.add_reaction('👎')

    elif message.content == 'big' or message.content == 'big big':
        await message.channel.send('chungus')

    elif message.content.lower().__contains__('z'):
        await message.channel.send('go to bed')

    elif message.content == '?ffroll':
        async_result = pool.apply_async(ffroll.roll)
        return_value = async_result.get()

        await message.channel.send(return_value)

    elif message.content == '?tray':
        await message.channel.send(client.get_user(395444424676605964))


client.run(token)
