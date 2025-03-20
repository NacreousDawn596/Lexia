import disnake
from disnake.ext import commands
import random

class Coinflip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="coinflip")
    async def coinflip_text(self, ctx):
        await ctx.send(f"🪙 The coin landed on **{random.choice(['Heads', 'Tails'])}**!")

    @commands.slash_command(name="coinflip", description="see ur luck :3")
    async def coinflip(self, inter: disnake.CommandInteraction):
        await inter.response.send_message(f"🪙 The coin landed on **{random.choice(['Heads', 'Tails'])}**!")

def setup(bot):
    bot.add_cog(Coinflip(bot))
