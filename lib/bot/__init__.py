from datetime import datetime

from discord import Intents
from discord import Embed, File
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound

from lib.db import db 


PREFIX = "+"
OWNER_IDS = [757239097583730709]


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)
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

    async def rules_reminder(self):
        channel = self.get_channel(808620454122225674)
        await channel.send("Do not Tag, DM, or add Staff as friends, because we are not your friends.")

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
            self.scheduler.add_job(self.rules_reminder, CronTrigger(day_of_week=0, hour=12, minute=0, second=0))
            self.scheduler.start()

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

            print("Bot Ready!")

        else:
            print("Bot Reconnected!")
            

    async def on_message(self, message):
        pass


bot = Bot()
        
