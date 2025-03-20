import disnake
from disnake.ext import commands
import random

class Match(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_message(self):
        compatibility = random.randint(0, 100)
        if compatibility < 30:
            return "Oof... not a great match. 😬", compatibility
        elif compatibility < 70:
            return "Not bad! Could work. 🤔", compatibility
        else:
            return "A match made in heaven! 💖", compatibility

    @commands.slash_command(name="match", description="Match with other users within the same server :3")
    async def match(
        self,
        inter: disnake.ApplicationCommandInteraction,
        user1: disnake.Member = commands.Param(default=None, description="Select the first user"),
        user2: disnake.Member = commands.Param(default=None, description="Select the second user")
    ):
        if user1 is None:
            non_bot_members = [member for member in inter.guild.members if not member.bot and member != inter.author]
            if not non_bot_members:
                await inter.response.send_message("No other non-bot members to match with!", ephemeral=True)
                return
            user1 = random.choice(non_bot_members)

        if user2 is None:
            user2 = inter.author

        if user1 == user2:
            await inter.response.send_message("You can't match a user with themselves! 😅", ephemeral=True)
            return

        message, compatibility = self.get_message()

        embed = disnake.Embed(
            title=f"{user1.display_name} 💞 {user2.display_name}",
            description=f"**Compatibility:** {compatibility}%\n{message}",
            color=disnake.Color.random()  # Random color for each match
        )
        embed.set_footer(text=f"Requested by {inter.author.display_name}", icon_url=inter.author.avatar.url)

        await inter.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(Match(bot))
