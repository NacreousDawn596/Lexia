import disnake
from disnake.ext import commands
from disnake.ui import Button, View

class ReactRoleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Hardcoded reaction role configurations
        self.reaction_role_configs = [
            {
                "description": "React to get a color Role :3",
                "roles": {
                    "🩷": 1353035548389933077,  # Replace with your role IDs
                    "💜": 1353035546959548427,
                    "🧡": 1353035539057606687,
                    "🩵": 1353035545164513383,
                    "💚": 1353035543985913966,
                    "💛": 1353035541913927791,
                    "❤️":  1353035537333616693
                }
            },
            {
                "description": "React to set ur pronouns",
                "roles": {
                    "👧": 1353035567872348232,
                    "👦": 1353035565322211409,
                    "🧒": 1353035566605926470
                }
            },
            {
                "description": "set your age interval",
                "roles": {
                    "🔞": 1353035561945792582,
                    "🍻": 1353035563481042944
                }
            }
        ]

    async def create_reactrole_view(self, roles):
        """Create and return a persistent reaction role view."""
        view = View(timeout=None)  # No timeout for persistent views

        # Add buttons for each role
        for emoji, role_id in roles.items():
            button = Button(
                style=disnake.ButtonStyle.secondary,
                label=emoji,
                custom_id=f"reactrole_{role_id}",  # Unique custom_id for each role
                emoji=emoji
            )
            view.add_item(button)

        return view

    @commands.slash_command()
    @commands.has_permissions(administrator=True)
    async def setup_reactroles(self, ctx):
        """
        Setup multiple reaction role messages from hardcoded configurations.
        """
        # Loop through each configuration and create a reaction role message
        for config in self.reaction_role_configs:
            embed = disnake.Embed(
                title="Get Roles",
                description=config["description"],
                color=disnake.Color.orange()
            )

            # Create the view
            view = await self.create_reactrole_view(config["roles"])

            # Send the message
            await ctx.send(embed=embed, view=view)

        await ctx.send("All reaction role messages have been set up!", ephemeral=True)

    @commands.Cog.listener()
    async def on_ready(self):
        """Reattach persistent views when the bot starts up."""
        for config in self.reaction_role_configs:
            view = await self.create_reactrole_view(config["roles"])
            self.bot.add_view(view)  # Add the persistent view to the bot

    @commands.Cog.listener()
    async def on_button_click(self, interaction: disnake.MessageInteraction):
        """Handle button clicks for reaction roles."""
        if interaction.component.custom_id.startswith("reactrole_"):
            role_id = int(interaction.component.custom_id.split("_")[1])  # Extract role ID
            role = interaction.guild.get_role(role_id)

            if role:
                if role in interaction.user.roles:
                    await interaction.user.remove_roles(role)
                    await interaction.response.send_message(
                        f"Removed the {role.name} role!", ephemeral=True
                    )
                else:
                    await interaction.user.add_roles(role)
                    await interaction.response.send_message(
                        f"Added the {role.name} role!", ephemeral=True
                    )
            else:
                await interaction.response.send_message(
                    "Role not found!", ephemeral=True
                )

def setup(bot):
    bot.add_cog(ReactRoleCog(bot))