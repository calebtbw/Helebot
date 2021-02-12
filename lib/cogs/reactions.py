from discord.ext.commands import Cog

class Reactions(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.colours = {
                "❤️": self.bot.guild.get_role(809779790105935902), # Daemon 110
                "💛": self.bot.guild.get_role(809779797458419742), # Daemon 111
            }
            self.reaction_message = await self.bot.get_channel(809776178294030357).fetch_message(809779125044248676)
            self.bot.cogs_ready.ready_up("reactions")

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

   # @Cog.listener()
   # async def on_raw_reaction_remove(self, payload):
   #     if self.bot.ready and payload.message_id == self.reaction_message.id:
   #         member = self.bot.guild.get_member(payload.user_id)
   #         await member.remove_roles(self.colours[payload.emoji.name], reason="Daemon Role Reaction.")


def setup(bot):
    bot.add_cog(Reactions(bot))