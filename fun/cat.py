import disnake
from disnake.ext import commands
import requests

class Cat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def getCat(self):
        return requests.get("https://api.thecatapi.com/v1/images/search").json()[0]['url']

    @commands.command(name="cat")
    async def cat_text(self, ctx):
        await ctx.send(self.getCat())

    @commands.slash_command(name="cat", description="get a cat picturr")
    async def cat(self, inter: disnake.CommandInteraction):
        await inter.response.send_message(self.getCat())

def setup(bot):
    bot.add_cog(Cat(bot))
