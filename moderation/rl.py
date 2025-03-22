import disnake
from disnake.ext import commands
import asyncio

class RoleManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def is_bot_owner(interaction: disnake.ApplicationCommandInteraction) -> bool:
        return await interaction.bot.is_owner(interaction.user)

    @commands.slash_command()
    @commands.check(is_bot_owner)
    async def delete_duplicate_roles(
        self,
        interaction: disnake.ApplicationCommandInteraction
    ):
        """Delete duplicate roles in the server (Bot Owner Only)"""
        await interaction.response.defer()

        guild = interaction.guild
        if not guild:
            await interaction.edit_original_message("This command must be used in a server.")
            return

        # Check bot permissions
        bot_member = guild.get_member(self.bot.user.id)
        if not bot_member.guild_permissions.manage_roles:
            await interaction.edit_original_message("I need the `Manage Roles` permission to do this.")
            return

        # Get all roles (excluding @everyone)
        roles = [role for role in guild.roles if not role.is_default()]
        bot_top_role = bot_member.top_role

        # Track duplicates
        seen_names = set()
        duplicates = []
        for role in roles:
            if role.name in seen_names and role < bot_top_role:  # Ensure bot can delete the role
                duplicates.append(role)
            else:
                seen_names.add(role.name)

        if not duplicates:
            await interaction.edit_original_message("No duplicate roles found!")
            return

        # Delete duplicates
        deleted_count = 0
        for role in duplicates:
            try:
                await role.delete(reason="Removing duplicate role")
                deleted_count += 1
                await asyncio.sleep(1.0)  # Avoid rate limits
            except disnake.HTTPException as e:
                await interaction.edit_original_message(f"Failed to delete role {role.name}: {str(e)}")
                return

        await interaction.edit_original_message(f"Deleted {deleted_count} duplicate roles!")

def setup(bot):
    bot.add_cog(RoleManager(bot))