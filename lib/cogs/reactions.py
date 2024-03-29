from datetime import datetime, timedelta

from discord import Embed
from discord.ext.commands import Cog
from discord.ext.commands import command, has_permissions


# # Number emotes.
# "1️⃣", "2⃣", "3⃣", "4⃣", "5⃣","6⃣", "7⃣", "8⃣", "9⃣", "🔟"


numbers = ("1️⃣", "2⃣", "3⃣", "4⃣", "5⃣",
		   "6⃣", "7⃣", "8⃣", "9⃣", "🔟")


class Reactions(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.polls = []

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.colours = {
                "❤️": self.bot.guild.get_role(809779790105935902), # Daemon 110
                "💛": self.bot.guild.get_role(809779797458419742), # Daemon 111
            }
            self.reaction_message = await self.bot.get_channel(809776178294030357).fetch_message(809779125044248676)
            self.bot.cogs_ready.ready_up("reactions")

    @command(name="createpoll")
    @has_permissions(manage_guild=True)
    async def create_poll(self, ctx, hours: int, question: str, *options):
        if len(options) > 10:
            await ctx.send("You can only have a maximum of 10 options!")

        else:
            embed = Embed(title="Poll Question",
                          description=question,
                          colour=ctx.author.colour,
                          timestamp=datetime.utcnow())

            fields = [("Options", "\n".join([f"{numbers[idx]} {option}" for idx, option in enumerate(options)]), False),
                      ("Instructions", "React to cast a vote!", False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            message = await ctx.send(embed=embed)

            for emoji in numbers[:len(options)]:
                await message.add_reaction(emoji)

            self.polls.append((message.channel.id, message.id))

            self.bot.scheduler.add_job(self.complete_poll, "date", run_date=datetime.now()+timedelta(seconds=hours),
                                       args=[message.channel.id, message.id])

    async def complete_poll(self, channel_id, message_id):
        message = await self.bot.get_channel(channel_id).fetch_message(message_id)

        most_voted = max(message.reactions, key=lambda r: r.count)

        await message.channel.send(f"Poll Over! Option {most_voted.emoji} was the most popular with {most_voted.count-1:,} votes!")
        self.polls.remove((message.channel.id, message.id))

   # @Cog.listener()
   # async def on_reaction_add(self, reaction, user):
   #     print(f"{user.display_name} reacted with {reaction.emoji}")

   # @Cog.listener()
   # async def on_reaction_remove(self, reaction, user):
   #     print(f"{user.display_name} removed their reaction of {reaction.emoji}")

    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if self.bot.ready and payload.message_id == self.reaction_message.id:
            current_colours = filter(lambda r: r in self.colours.values(), payload.member.roles)
            await payload.member.remove_roles(*current_colours, reason="Daemon Role Reaction.")
            await payload.member.add_roles(self.colours[payload.emoji.name], reason="Daemon Role Reaction.")       
            await self.reaction_message.remove_reaction(payload.emoji, payload.member)

        elif payload.message_id in (poll[1] for poll in self.polls):
            message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)

            for reaction in message.reactions:
                if (not payload.member.bot
                    and payload.member in await reaction.users().flatten()
                    and reaction.emoji != payload.emoji.name):
                    await message.remove_reaction(reaction.emoji, payload.member)
        
   # @Cog.listener()
   # async def on_raw_reaction_remove(self, payload):
   #     if self.bot.ready and payload.message_id == self.reaction_message.id:
   #         member = self.bot.guild.get_member(payload.user_id)
   #         await member.remove_roles(self.colours[payload.emoji.name], reason="Daemon Role Reaction.")


def setup(bot):
    bot.add_cog(Reactions(bot))