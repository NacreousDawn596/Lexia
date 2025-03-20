import disnake
from disnake.ext import commands
import requests

class Joke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def getJoke(self):
        result = requests.get("https://v2.jokeapi.dev/joke/Any").json()
        return result['setup'], result['delivery']

    @commands.command(name="joke")
    async def joke_command(self, ctx):
        setup, delivery = self.getJoke()
        await ctx.send(f"> {setup}\n- {delivery}")

    @commands.slash_command(name="joke", description="Send a hilarious joke lol")
    async def joke_slash(self, inter: disnake.CommandInteraction):
        setup, delivery = self.getJoke()
        await inter.response.send_message(f"> {setup}\n- {delivery}")

def setup(bot):
    bot.add_cog(Joke(bot))