# pay.py
import disnake
from disnake.ext import commands

class Pay(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="pay", description="Send coins to another user")
    async def pay_slash(
        self,
        inter: disnake.ApplicationCommandInteraction,
        user: disnake.Member,
        amount: int = commands.Param(gt=0, description="Amount to send")
    ):
        await self.handle_payment(inter, user, amount)

    @commands.command(name="pay", aliases=["send"], help="Send coins to another user\nUsage: !pay @user <amount>")
    async def pay_text(self, ctx: commands.Context, user: disnake.Member, amount: int):
        await self.handle_payment(ctx, user, amount)

    async def handle_payment(self, source: commands.Context | disnake.ApplicationCommandInteraction, user: disnake.Member, amount: int):
        if isinstance(source, disnake.ApplicationCommandInteraction):
            ctx = source
            is_slash = True
        else:
            ctx = source
            is_slash = False

        if user.bot:
            return await ctx.response.send_message("You can't pay bots!") if is_slash else await ctx.send("You can't pay bots!")

        if user == ctx.author:
            msg = "You can't pay yourself!"
            return await ctx.response.send_message(msg, ephemeral=True) if is_slash else await ctx.send(msg)

        sender_balance = self.bot.economy.get_user_balance(ctx.guild.id, ctx.author.id)
        
        if sender_balance < amount:
            msg = f"You don't have enough coins! Your balance: {sender_balance}"
            return await ctx.response.send_message(msg, ephemeral=True) if is_slash else await ctx.send(msg)

        self.bot.economy.add_coins_to_user(ctx.guild.id, ctx.author.id, -amount)
        self.bot.economy.add_coins_to_user(ctx.guild.id, user.id, amount)

        embed = disnake.Embed(
            title="💸 Payment Successful",
            color=disnake.Color.green()
        )
        embed.add_field(
            name="Transaction Details",
            value=f"**From:** {ctx.author.mention}\n**To:** {user.mention}\n**Amount:** {amount} coins",
            inline=False
        )
        embed.add_field(
            name="New Balances",
            value=(
                f"{ctx.author.display_name}: `{sender_balance - amount}`\n"
                f"{user.display_name}: `{self.bot.economy.get_user_balance(ctx.guild.id, user.id)}`"
            ),
            inline=False
        )
        embed.set_thumbnail(url=ctx.author.display_avatar.url)

        if is_slash:
            await ctx.response.send_message(embed=embed)
        else:
            await ctx.send(embed=embed)

    @pay_slash.error
    @pay_text.error
    async def pay_error(self, ctx: commands.Context | disnake.ApplicationCommandInteraction, error):
        is_slash = isinstance(ctx, disnake.ApplicationCommandInteraction)
        msg = ""

        if isinstance(error, commands.MissingRequiredArgument):
            msg = "Missing required arguments! Usage: " + ("`/pay <user> <amount>`" if is_slash else "`!pay @user <amount>`")
        elif isinstance(error, commands.BadArgument):
            msg = "Invalid user or amount format!"
        elif isinstance(error, commands.CommandInvokeError):
            msg = f"Error processing payment: {str(error.original)}"
        else:
            msg = f"An error occurred: {str(error)}"

        if is_slash:
            await ctx.response.send_message(msg, ephemeral=True)
        else:
            await ctx.send(msg)

def setup(bot: commands.Bot):
    bot.add_cog(Pay(bot))