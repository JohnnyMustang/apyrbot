import asyncio
import discord
import json
import hashlib
import aiohttp

class NamerBot(discord.Client):
    def __init__(self, config_path: str, pokenames_path: str, *args, **kwargs):
        self.config_path = config_path
        with open(self.config_path) as f:
            self.configs = json.load(f)
        self.prefix = self.configs['command_prefix']
        with open(pokenames_path, 'r', encoding='utf-8') as f:
            self.pokenames = json.load(f)
        super().__init__()
    @self.event
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
        self.sess = aiohttp.ClientSession(loop=self.loop)