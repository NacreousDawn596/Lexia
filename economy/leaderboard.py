import disnake
from disnake.ext import commands

class LeaderboardCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="leaderboard", description="Display the top users in this guild.")
    async def leaderboard(self, inter: disnake.ApplicationCommandInteraction):
        guild_id = inter.guild.id
        economy = self.bot.economy.get_guild_economy(guild_id)

        user_balances = {
            user_id: balance
            for user_id, balance in economy.items()
            if not user_id.endswith("_last_daily")
        }

        sorted_users = sorted(user_balances.items(), key=lambda x: x[1], reverse=True)

        embed = disnake.Embed(
            title="🏆 Leaderboard",
            description="Top users in this guild:",
            color=disnake.Color.gold()
        )

        for rank, (user_id, balance) in enumerate(sorted_users[:10], start=1):  # Top 10 users
            user = await self.bot.fetch_user(user_id)
            embed.add_field(
                name=f"{rank}. {user.display_name}",
                value=f"**{balance}** coins",
                inline=False
            )

        await inter.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(LeaderboardCog(bot))