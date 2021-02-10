from typing import Optional

from discord import Member
from discord.ext.commands import Cog
from discord.ext.commands import BadArgument
from discord.ext.commands import command


class Test(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="hello", aliases=["hi"])
    async def say_hello(self, ctx):
        await ctx.send(f"Hello, {ctx.author.mention}!")

    @command(name="quote", aliases=["say"]) 
    async def say_quote(self, ctx): 
        await ctx.send(f"When {ctx.author.mention} pursues something, nothing stands in his way.")

    @command(name="godstatus", aliases=["gstatus"])
    async def say_godstatus(self, ctx):
        await ctx.send(f"{ctx.author.mention} is a God.")

    @command(name="devstatus", aliases=["dstatus"])
    async def say_devstatus(self, ctx):
        await ctx.send(f"{ctx.author.mention} for JR Discord Developer at GGServers")

    @command(name="jobapp", aliases=["japp"])
    async def say_jobapp(self, ctx):
        await ctx.send(f"I couldn't agree more {ctx.author.mention} , some people's job applications are horrible. Unlike yours.")

    @command(name="respect", aliases=["res"])
    async def say_respect(self, ctx):
        await ctx.send(f"We gather today to pay respects to that one guy who titled his job application, 'Staff Pay'.") 

    @command(name="slap", aliases=["spank"])
    async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "reasons known only to himself/herself"):
        await ctx.send(f"{ctx.author.mention} slapped {member.mention} for {reason}")

    @slap_member.error
    async def slap_member_error(self, ctx, exc):
        if isinstance(exc, BadArgument):
            await ctx.send("Unable to locate victim.")

    @command(name="ghub")
    async def say_ghub(self, ctx):
        await ctx.send(f"| Github: https://github.com/calebtbw | Mostly Java Projects")

    @command(name="glab")
    async def say_glab(self, ctx):
        await ctx.send(f"| Gitlab: https://gitlab.com/calebtaybw | Where Python Begins")
        
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("test")


def setup(bot):
    bot.add_cog(Test(bot))