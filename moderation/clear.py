import disnake
from disnake.ext import commands

class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="clear", description="Clear a specified number of messages")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        if amount <= 0:
            await ctx.send("Please provide a positive number of messages to delete.")
            return
        await ctx.channel.purge(limit=amount + 1)  # +1 to include the command message
        await ctx.send(f"Cleared {amount} messages.", delete_after=5)

    @commands.slash_command(name="clear", description="Clear a specified number of messages")
    @commands.has_permissions(manage_messages=True)
    async def clear_slash(self, inter: disnake.CommandInteraction, amount: int):
        if amount <= 0:
            await inter.response.send_message("Please provide a positive number of messages to delete.", ephemeral=True)
            return
        await inter.channel.purge(limit=amount + 1)
        await inter.response.send_message(f"Cleared {amount} messages.", ephemeral=True)

    @clear.error
    @clear_slash.error
    async def clear_error(self, ctx_or_inter, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx_or_inter.send("You do not have permission to use this command.", ephemeral=True)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx_or_inter.send("Please provide the number of messages to delete.", ephemeral=True)
        elif isinstance(error, commands.BadArgument):
            await ctx_or_inter.send("Invalid argument provided.", ephemeral=True)
        else:
            await ctx_or_inter.send(f"An error occurred: {error}", ephemeral=True)

def setup(bot):
    bot.add_cog(Clear(bot))