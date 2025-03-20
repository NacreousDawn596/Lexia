import disnake
from disnake.ext import commands

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hewwoo")
    async def hello(self, ctx):
        await ctx.send("Hello, world!")

    @commands.slash_command(name="hewwoo", description="send a greeting message")
    async def hello_slash(self, inter: disnake.CommandInteraction):
        await inter.response.send_message("Hello, world! This is a slash command.")

def setup(bot):
    bot.add_cog(Greetings(bot))
