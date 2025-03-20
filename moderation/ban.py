import disnake
from disnake.ext import commands

class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ban", description="Ban a member from the server")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: disnake.Member, *, reason=None):
        if member == ctx.author:
            await ctx.send("You cannot ban yourself.")
            return
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} has been banned. Reason: {reason}")

    @commands.slash_command(name="ban", description="Ban a member from the server")
    @commands.has_permissions(ban_members=True)
    async def ban_slash(self, inter: disnake.CommandInteraction, member: disnake.Member, reason: str = None):
        if member == inter.author:
            await inter.response.send_message("You cannot ban yourself.", ephemeral=True)
            return
        await member.ban(reason=reason)
        await inter.response.send_message(f"{member.mention} has been banned. Reason: {reason}")

    @ban.error
    @ban_slash.error
    async def ban_error(self, ctx_or_inter, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx_or_inter.send("You do not have permission to use this command.", ephemeral=True)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx_or_inter.send("Please mention a member to ban.", ephemeral=True)
        elif isinstance(error, commands.BadArgument):
            await ctx_or_inter.send("Invalid member provided.", ephemeral=True)
        else:
            await ctx_or_inter.send(f"An error occurred: {error}", ephemeral=True)

def setup(bot):
    bot.add_cog(Ban(bot))