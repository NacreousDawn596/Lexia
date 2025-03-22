import disnake
from disnake.ext import commands
from disnake.ui import Button, View

class VerificationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.verified_role_id = 1353035506027335722  # Replace with your role ID

    async def create_verify_view(self):
        """Create and return the persistent verification view."""
        view = View(timeout=None)  # No timeout for persistent views
        view.add_item(Button(style=disnake.ButtonStyle.green, label="Verify", custom_id="verify_button"))
        return view

    @commands.slash_command()
    @commands.has_permissions(administrator=True)
    async def setup_verify(self, ctx):
        """Setup verification button"""
        embed = disnake.Embed(
            title="Verify Account",
            description="Click the button below to verify yourself!",
            color=disnake.Color.blurple()
        )
        view = await self.create_verify_view()
        await ctx.send(embed=embed, view=view)

    @commands.Cog.listener()
    async def on_ready(self):
        """Reattach the persistent view when the bot starts up."""
        if not self.bot.persistent_views:
            view = await self.create_verify_view()
            self.bot.add_view(view)  # Add the persistent view to the bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction: disnake.MessageInteraction):
        """Handle button clicks for verification."""
        if interaction.component.custom_id == "verify_button":
            role = interaction.guild.get_role(self.verified_role_id)
            if role:
                await interaction.user.add_roles(role)
                await interaction.response.send_message(
                    "You've been verified!", ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    "Verification role not found!", ephemeral=True
                )

def setup(bot):
    bot.add_cog(VerificationCog(bot))