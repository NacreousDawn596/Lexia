import disnake
from disnake.ext import commands
import time

class MessageListenerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_cooldown = {}  # To track message cooldowns

    @commands.Cog.listener()
    async def on_message(self, message):
        """Grant coins for sending messages (with cooldown)."""
        if message.author.bot:  # Ignore bot messages
            return

        guild_id = message.guild.id
        user_id = message.author.id

        # Check cooldown
        last_message_time = self.message_cooldown.get(user_id, 0)
        now = time.time()
        if now - last_message_time < 60:  # 60 seconds cooldown
            return

        # Grant coins
        self.bot.economy.add_coins_to_user(guild_id, user_id, 10)  # Grant 10 coins per message
        self.message_cooldown[user_id] = now

def setup(bot):
    bot.add_cog(MessageListenerCog(bot))