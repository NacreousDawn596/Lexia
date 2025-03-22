import disnake
from disnake.ext import commands

class BalanceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="balance", description="Check your or another user's balance.")
    async def balance(
        self,
        inter: disnake.ApplicationCommandInteraction,
        user: disnake.Member = None
    ):
        """Check a user's balance."""
        guild_id = inter.guild.id
        target_user = user or inter.author
        balance = self.bot.economy.get_user_balance(guild_id, target_user.id)

        embed = disnake.Embed(
            title="💰 Balance",
            description=f"{target_user.mention}'s balance is **{balance}** coins.",
            color=disnake.Color.blue()
        )
        embed.set_thumbnail(url=target_user.display_avatar.url)
        await inter.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(BalanceCog(bot))