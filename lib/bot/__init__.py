from datetime import datetime

from discord import Intents
from discord import Embed, File
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound

PREFIX = "+"
OWNER_IDS = [757239097583730709]


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        super().__init__(
            command_prefix=PREFIX, 
            owner_ids=OWNER_IDS,
            intents=Intents.all(),
        )

    def run(self, version):
        self.VERSION = version

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("Running Bot...")
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        print("Bot Connected!")

    async def on_disconnect(self):
        print("Bot Disconnected!")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong.")

        channel = self.get_channel(808620454122225674)
        await channel.send("An error occured.")   
        raise # type: ignore 

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            pass

        elif hasattr(exc, "original"):
            raise exc.original

        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(808533625016156220)
            print("Bot Ready!")

            channel = self.get_channel(808620454122225674)
            await channel.send("Now Online!")

            embed = Embed(title="Now Online!", description="CT Bot is running like a God.", 
                          colour=0xFF0000, timestamp=datetime.utcnow())
            fields = [("CT BOT", "0.0.3", True),
                      ("Made by:", "The unthinkable knowledge of a God.", True),
                      ("For:", "Me to realise I am actually a God.", False)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_author(name="Caleb T.", icon_url=self.guild.icon_url)
            embed.set_footer(text="Made with Python")    
            embed.set_thumbnail(url=self.guild.icon_url)
            embed.set_image(url=self.guild.icon_url)
            await channel.send(embed=embed)

            await channel.send(file=File("./data/images/logo.png"))

        else:
            print("Bot Reconnected!")
            

    async def on_message(self, message):
        pass


bot = Bot()
        
