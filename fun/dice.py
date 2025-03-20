import disnake
from disnake.ext import commands
import random

class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="dice")
    async def dice_text(self, ctx):
        await ctx.send(f"🎲 You rolled a **{random.randint(1, 6)}**!")

    @commands.slash_command(name="dice", description="Roll a dice (1-6)")
    async def dice(self, inter: disnake.CommandInteraction):
        await inter.response.send_message(f"🎲 You rolled a **{random.randint(1, 6)}**!")

def setup(bot):
    bot.add_cog(Dice(bot))
