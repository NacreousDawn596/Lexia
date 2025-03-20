import disnake
from disnake.ext import commands
from g4f.client import Client

class ImageGen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gpt_client = Client()

    async def generate_response(self, text):
        response = self.gpt_client.images.generate(
            model="flux",
            prompt=text,
            response_format="url"
        )

        return response.data[0].url

    @commands.command(name="imagegen")
    async def imagegen_text(self, ctx, *, message: str):
        async with ctx.channel.typing():
            response = await self.generate_response(message)
            await ctx.reply(response)

    @commands.slash_command(name="imagegen", description="generate images :3")
    async def imagegen(self, inter: disnake.CommandInteraction, message: str):
        await inter.response.defer()
        response = await self.generate_response(message)
        await inter.followup.send(response)

def setup(bot):
    bot.add_cog(ImageGen(bot))