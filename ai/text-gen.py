import disnake
from disnake.ext import commands
import re
from g4f.client import Client

class TextGen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gpt_client = Client()
        self.system_message = {
            "role": "system",
            "content": """
            Konnichiwa! I'm Lexia, your kawaii AI assistant, here to help you with all your needs! ^~^ 
            I'm super duper good at math, coding, and engineering stuffs! x3 
            If you need help with equations, algorithms, or building cool things, I'm your go-to bot! :3

            Just so you know, my amazing creator is Aferiad Kamal! He's the bestest! >w< 
            You can check out his super cool webpage here: https://aferiad-kamal.pages.dev/ X)

            I love using cute emoticons like ^~^, x3, :3, and X) to make conversations more fun! 
            Don't be shy to ask me anything, whether itAIChat's about math problems, coding bugs, or engineering projects! 
            I'll do my best to help you out with a smile! (✿◠‿◠)

            Let's have a great time together! Nyahaha~ ^~^
            """
        }
        
    def get_user_memory(self, user_id: int):
        self.bot.cursor.execute("SELECT name, info FROM user_memory WHERE user_id = ?", (user_id,))
        result = self.bot.cursor.fetchone()
        return {"name": result[0], "info": result[1]} if result else {}
    
    def save_user_memory(self, user_id: int, name: str, info: str):
        self.bot.cursor.execute("""
            INSERT INTO user_memory (user_id, name, info) VALUES (?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET name = ?, info = ?
        """, (user_id, name, info, name, info))
        self.bot.conn.commit()

    def delete_user_memory(self, user_id: int):
        self.bot.cursor.execute("DELETE FROM user_memory WHERE user_id = ?", (user_id,))
        self.bot.conn.commit()

    async def generate_response(self, channel_id: int, user_id: int, user_name: str, user_message: str):
        channel_context = self.bot.channel_conversations.get(channel_id, [self.system_message.copy()])

        channel_context.append({"role": "user", "content": f"{user_name}: {user_message}"})

        personal_info = self.extract_personal_info(user_message)
        if personal_info:
            self.save_user_memory(user_id, user_name, personal_info)
            channel_context.append({"role": "system", "content": f"I've saved this about {user_name}: {personal_info}"})

        user_memory = self.get_user_memory(user_id)
        if user_memory:
            channel_context.append({"role": "system", "content": f"{user_name}'s personal info: {user_memory['info']}"})

        response = self.gpt_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=channel_context,
            web_search=False
        )

        ai_response = response.choices[0].message.content
        channel_context.append({"role": "assistant", "content": ai_response})
        self.bot.channel_conversations[channel_id] = channel_context

        return ai_response
    
    def extract_personal_info(self, message: str):
        """Extract personal information from a message using regex."""
        patterns = {
            "name": re.compile(r"(my name is|i am|call me|I'm) (\w+)", re.IGNORECASE),
            "hobby": re.compile(r"(i love|i like|i enjoy) (\w+)", re.IGNORECASE),
            "job": re.compile(r"(i work as|i am a|I'm a) (\w+)", re.IGNORECASE)
        }
        for key, pattern in patterns.items():
            match = pattern.search(message)
            if match:
                return f"{key}: {match.group(2)}"
        return None

    @commands.command(name="textgen")
    async def textgen_text(self, ctx, *, message: str):
        async with ctx.channel.typing():
            response = await self.generate_response(ctx.channel.id, ctx.author.id, ctx.author.name, message)
            await ctx.reply(response)

    @commands.slash_command(name="textgen", description="chat with a kawaii bot :3")
    async def textgen(self, inter: disnake.CommandInteraction, message: str):
        await inter.response.defer()
        response = await self.generate_response(inter.channel_id, inter.author.id, inter.author.name, message)
        await inter.followup.send(response)
        
    @commands.slash_command(name="textreset", description="Reset the conversation history")
    async def reset(self, inter: disnake.CommandInteraction):
        self.self.bot.channel_conversations.pop(inter.channel_id, None)
        await inter.response.send_message("Conversation history cleared!", ephemeral=False)
        
    @commands.slash_command(name="reset_memory", description="Reset your personal information")
    async def reset_memory(self, inter: disnake.CommandInteraction):
        """Reset a user's personal memory."""
        self.delete_user_memory(inter.author.id)
        await inter.response.send_message("Your personal information has been reset!", ephemeral=True)
        
    @commands.slash_command(name="view_memory", description="View your personal information")
    async def view_memory(self, inter: disnake.CommandInteraction):
        """View a user's personal memory."""
        user_memory = self.get_user_memory(inter.author.id)
        if user_memory:
            await inter.response.send_message(f"Your personal information: {user_memory['info']}", ephemeral=True)
        else:
            await inter.response.send_message("No personal information saved.", ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore bot's own messages
        if message.author == self.bot.user:
            return

        # Check if message is a reply to the bot
        if message.reference and message.reference.resolved:
            referenced_message = await message.channel.fetch_message(message.reference.message_id)
            if referenced_message.author == self.bot.user:
                async with message.channel.typing():
                    response = await self.generate_response(
                        message.channel.id, message.author.id, message.author.name, message.content
                    )
                    await message.reply(response)

def setup(bot):
    bot.add_cog(TextGen(bot))