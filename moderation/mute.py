import disnake
from disnake.ext import commands
from disnake.utils import get

class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mute", description="Mute a member")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: disnake.Member, *, reason=None):
        mute_role = get(ctx.guild.roles, name="Muted")  # Ensure you have a "Muted" role
        if not mute_role:
            await ctx.send("No 'Muted' role found. Please create one.")
            return
        await member.add_roles(mute_role, reason=reason)
        await ctx.send(f"{member.mention} has been muted. Reason: {reason}")

    @commands.slash_command(name="mute", description="Mute a member")
    @commands.has_permissions(manage_roles=True)
    async def mute_slash(self, inter: disnake.CommandInteraction, member: disnake.Member, reason: str = None):
        mute_role = get(inter.guild.roles, name="Muted")
        if not mute_role:
            await inter.response.send_message("No 'Muted' role found. Please create one.", ephemeral=True)
            return
        await member.add_roles(mute_role, reason=reason)
        await inter.response.send_message(f"{member.mention} has been muted. Reason: {reason}")

    @commands.command(name="unmute", description="Unmute a member")
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: disnake.Member):
        mute_role = get(ctx.guild.roles, name="Muted")
        if not mute_role:
            await ctx.send("No 'Muted' role found. Please create one.")
            return
        await member.remove_roles(mute_role)
        await ctx.send(f"{member.mention} has been unmuted.")

    @commands.slash_command(name="unmute", description="Unmute a member")
    @commands.has_permissions(manage_roles=True)
    async def unmute_slash(self, inter: disnake.CommandInteraction, member: disnake.Member):
        mute_role = get(inter.guild.roles, name="Muted")
        if not mute_role:
            await inter.response.send_message("No 'Muted' role found. Please create one.", ephemeral=True)
            return
        await member.remove_roles(mute_role)
        await inter.response.send_message(f"{member.mention} has been unmuted.")

    @mute.error
    @mute_slash.error
    @unmute.error
    @unmute_slash.error
    async def mute_error(self, ctx_or_inter, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx_or_inter.send("You do not have permission to use this command.", ephemeral=True)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx_or_inter.send("Please mention a member to mute/unmute.", ephemeral=True)
        elif isinstance(error, commands.BadArgument):
            await ctx_or_inter.send("Invalid member provided.", ephemeral=True)
        else:
            await ctx_or_inter.send(f"An error occurred: {error}", ephemeral=True)

def setup(bot):
    bot.add_cog(Mute(bot))