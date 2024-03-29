from datetime import datetime

from discord import Embed
from discord.ext.commands import Cog
from discord.ext.commands import command

class Log(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.logs_channel = self.bot.get_channel(809059328975175740)
            self.bot.cogs_ready.ready_up("log")

    @Cog.listener()
    async def on_user_update(self, before, after):
        if before.name != after.name:
            embed = Embed(title="Username change",
                          colour=after.colour,
                          timestamp=datetime.utcnow())
            
            fields = [("Before", before.name, False),
                      ("After", after.name, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.logs_channel.send(embed=embed)

        if before.discriminator != after.discriminator:
            embed = Embed(title="Discriminator Change",
                          colour=after.colour,
                          timestamp=datetime.utcnow())
            
            fields = [("Before", before.discriminator, False),
                      ("After", after.discriminator, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.logs_channel.send(embed=embed)


        if before.avatar_url != after.avatar_url:
            embed = Embed(title="Member Update",
                          description="Avatar Change (New Below | Old Right)",
                          colour=self.logs_channel.guild.get_member(after.id).colour,
                          timestamp=datetime.utcnow())

            embed.set_thumbnail(url=before.avatar_url)
            embed.set_image(url=after.avatar_url)

            await self.logs_channel.send(embed=embed)   

    @Cog.listener()
    async def on_member_update(self, before, after):
        if before.display_name != after.display_name:
            embed = Embed(title="Nickname Change",
                          colour=after.colour,
                          timestamp=datetime.utcnow())
            
            fields = [("Before", before.display_name, False),
                      ("After", after.display_name, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.logs_channel.send(embed=embed)

        elif before.roles != after.roles:
            embed = Embed(title="Role Update",
                          colour=after.colour,
                          timestamp=datetime.utcnow())
            
            fields = [("Before", ", ".join([r.mention for r in before.roles]), False),
                      ("After", ", ".join([r.mention for r in after.roles]), False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.logs_channel.send(embed=embed)

    @Cog.listener()
    async def on_message_edit(self, before, after):
        if not after.author.bot:
            if before.content != after.content:
                embed = Embed(title="Message Edit",
                              description=f"Edited by {after.author.display_name}",
                              colour=after.author.colour,
                              timestamp=datetime.utcnow())
            
            fields = [("Before", before.content, False),
                      ("After", after.content, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.logs_channel.send(embed=embed)
                

    @Cog.listener()
    async def on_message_delete(self, message):
        if not message.author.bot:
            embed = Embed(title="Message Deletion",
                          description=f"Deleted by {message.author.display_name}",
                          colour=message.author.colour,
                          timestamp=datetime.utcnow())
            
            fields = [("Content", message.content, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.logs_channel.send(embed=embed)



def setup(bot):
    bot.add_cog(Log(bot))