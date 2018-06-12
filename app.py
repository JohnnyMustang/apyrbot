import asyncio
import discord
from discord.ext import commands
import json
import hashlib

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

class NamerBot(discord.Client):
    def __init__(self, config_path: str, pokenames_path: str, *args, **kwargs):
        self.config_path = config_path
        with open(self.config_path) as f:
            self.configs = json.load(f)
        self.prefix = self.configs['command_prefix']
        with open(pokenames_path, 'r', encoding='utf-8') as f:
            self.pokenames = json.load(f)
        super().__init__()

    def run(self):
        super().run(self.configs['token'])    

    async def match(self, url):
        async with await self.sess.get(url) as resp:
            dat = await resp.content.read()
        m = hashlib.md5(dat).hexdigest()
        return self.pokenames[m]

    async def on_message(self, message):
        if message.author.id == 365975655608745985:
            emb = message.embeds[0]
            try:
                embcheck = emb.title.startswith('A wild')
            except AttributeError:
                return    
            if embcheck:
                name = await self.match(emb.image.url.split('?')[0])
                name = name.title()
            await message.channel.send(name)

    async def on_ready(self):
        print("NamerBot is online!")

        self.ready = True

        @bot.command()
async def add(ctx, a: int, b: int):
    await ctx.send(a+b)

@bot.command()
async def multiply(ctx, a: int, b: int):
    await ctx.send(a*b)

@bot.command()
async def greet(ctx):
    await ctx.send(":smiley: :wave: Hello, there!")

@bot.command()
async def cat(ctx):
    await ctx.send("https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif")

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="nice bot", description="Nicest bot there is ever.", color=0xeee657)
    
    # give info about you here
    embed.add_field(name="Author", value="<YOUR-USERNAME>")
    
    # Shows the number of servers the bot is member of.
    embed.add_field(name="Server count", value=f"{len(bot.guilds)}")

    # give users a link to invite thsi bot to their server
    embed.add_field(name="Invite", value="[Invite link](<insert your OAuth invitation link here>)")

    await ctx.send(embed=embed)

bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="nice bot", description="A Very Nice bot. List of commands are:", color=0xeee657)

    embed.add_field(name="$add X Y", value="Gives the addition of **X** and **Y**", inline=False)
    embed.add_field(name="$multiply X Y", value="Gives the multiplication of **X** and **Y**", inline=False)
    embed.add_field(name="$greet", value="Gives a nice greet message", inline=False)
    embed.add_field(name="$cat", value="Gives a cute cat gif to lighten up the mood.", inline=False)
    embed.add_field(name="$info", value="Gives a little info about the bot", inline=False)
    embed.add_field(name="$help", value="Gives this message", inline=False)

    await ctx.send(embed=embed)

bot.run('process.env.TOKEN')
