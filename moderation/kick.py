import disnake
from disnake.ext import commands

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kick", description="Kick a member from the server")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: disnake.Member, *, reason=None):
        if member == ctx.author:
            await ctx.send("You cannot kick yourself.")
            return
        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} has been kicked. Reason: {reason}")

    @commands.slash_command(name="kick", description="Kick a member from the server")
    @commands.has_permissions(kick_members=True)
    async def kick_slash(self, inter: disnake.CommandInteraction, member: disnake.Member, reason: str = None):
        if member == inter.author:
            await inter.response.send_message("You cannot kick yourself.", ephemeral=True)
            return
        await member.kick(reason=reason)
        await inter.response.send_message(f"{member.mention} has been kicked. Reason: {reason}")

    @kick.error
    @kick_slash.error
    async def kick_error(self, ctx_or_inter, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx_or_inter.send("You do not have permission to use this command.", ephemeral=True)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx_or_inter.send("Please mention a member to kick.", ephemeral=True)
        elif isinstance(error, commands.BadArgument):
            await ctx_or_inter.send("Invalid member provided.", ephemeral=True)
        else:
            await ctx_or_inter.send(f"An error occurred: {error}", ephemeral=True)

def setup(bot):
    bot.add_cog(Kick(bot))