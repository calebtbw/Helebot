from asyncio import sleep
from datetime import datetime
from glob import glob

from discord import Intents
from discord import Embed, File, DMChannel
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.errors import HTTPException, Forbidden
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import Context
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument)

from lib.db import db


PREFIX = "+"
OWNER_IDS = [757239097583730709]
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)

class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"{cog} cog ready!")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])

class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)
        super().__init__(
            command_prefix=PREFIX, 
            owner_ids=OWNER_IDS,
            intents=Intents.all(),
        )

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f" {cog} cog loaded!")

        print("Setup Complete!")

    def run(self, version):
        self.VERSION = version

        print("Running Setup...")
        self.setup()

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("Running Bot...")
        super().run(self.TOKEN, reconnect=True)

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)

        if ctx.command is not None and ctx.guild is not None:
            if self.ready:
                await self.invoke(ctx)

            else:
                await ctx.send("Not ready for commands. Moment please.")

    async def rules_reminder(self):
        await self.stdout.send("Do not Tag, DM, or add Staff as friends, because we are not your friends.")

    async def on_connect(self):
        print("Bot Connected!")

    async def on_disconnect(self):
        print("Bot Disconnected!")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong.")

        await self.stdout.send("An error occured.")   
        
        raise # type: ignore 

    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
            pass

        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send("One of more required arguments are missing!")

        elif isinstance(exc.original, HTTPException):
            await ctx.send("Unable to send message.")

        elif isinstance(exc.original, Forbidden):
            await ctx.send("No permission to do that.")

        else:
            raise exc.original

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(808533625016156220)
            self.scheduler.add_job(self.rules_reminder, CronTrigger(day_of_week=0, hour=12, minute=0, second=0))
            self.stdout = self.get_channel(808620454122225674)
            self.scheduler.start()


            #embed = Embed(title="Now Online!", description="CT Bot is running like a God.", 
            #              colour=0xFF0000, timestamp=datetime.utcnow())
            #fields = [("CT BOT", "1.0.2", True),
            #          ("Made by:", "The unthinkable knowledge of a God.", True),
            #          ("For:", "Me to realise I am actually a God.", False)]
            #for name, value, inline in fields:
            #    embed.add_field(name=name, value=value, inline=inline)
            #embed.set_author(name="Caleb T.", icon_url=self.guild.icon_url)
            #embed.set_footer(text="Made with Python")    
            #embed.set_thumbnail(url=self.guild.icon_url)
            #embed.set_image(url=self.guild.icon_url)
            #await channel.send(embed=embed)

            #await channel.send(file=File("./data/images/logo.png"))


            while not self.cogs_ready.all_ready():
                await sleep(0.5)
            
            await self.stdout.send("Now Online!")
            self.ready = True
            print("Bot Ready!")

        else:
            print("Bot Reconnected!")
            

    async def on_message(self, message):       
        if not message.author.bot:
            if isinstance(message.channel, DMChannel):
                if len(message.content) < 50:
                    await message.channel.send("Your message should be at least 50 characters in length.")

                else:
                    member = self.guild.get_member(message.author.id)
                    embed = Embed(title="ModMail",
                                  colour=member.colour,
                                  timestamp=datetime.utcnow())
                    
                    embed.set_thumbnail(url=member.avatar_url)

                    fields = [("Member", member.display_name, False),
                              ("Message", message.content, False)]

                    for name, value, inline in fields:
                        embed.add_field(name=name, value=value, inline=inline)
                    
                    mod = self.get_cog("Mod")
                    await mod.logs_channel.send(embed=embed)
                    await message.channel.send("Message relayed to Moderators.")

            else:
                await self.process_commands(message)


bot = Bot()
        
