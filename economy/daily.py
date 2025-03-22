import disnake
from disnake.ext import commands
import time
from datetime import datetime

class DailyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="daily", description="Claim your daily coins.")
    async def daily(self, inter: disnake.ApplicationCommandInteraction):
        """Claim daily coins."""
        guild_id = inter.guild.id
        user_id = inter.author.id
        economy = self.bot.economy.get_guild_economy(guild_id)

        last_daily = economy.get(f"{user_id}_last_daily", 0)
        now = time.time()
        if now - last_daily < 86400:  # 86400 seconds = 1 day
            next_daily = datetime.fromtimestamp(last_daily + 86400).strftime("%Y-%m-%d %H:%M:%S")
            embed = disnake.Embed(
                title="⏳ Daily Reward Cooldown",
                description=f"You've already claimed your daily reward. You can claim again at **{next_daily}**.",
                color=disnake.Color.orange()
            )
            await inter.response.send_message(embed=embed)
            return

        economy[f"{user_id}_last_daily"] = now
        self.bot.economy.add_coins_to_user(guild_id, user_id, 100)  # Grant 100 coins
        balance = self.bot.economy.get_user_balance(guild_id, user_id)

        embed = disnake.Embed(
            title="🎉 Daily Reward Claimed",
            description=f"You claimed your daily reward of **100 coins**! Your new balance is **{balance}** coins.",
            color=disnake.Color.green()
        )
        embed.set_thumbnail(url=inter.author.display_avatar.url)
        await inter.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(DailyCog(bot))