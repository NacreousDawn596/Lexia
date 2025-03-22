import disnake
from disnake.ext import commands
from g4f.client import Client

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gpt_client = Client()
        self.system_message = {
            "role": "system",
            "content": """
            Konnichiwa! I'm your kawaii AI assistant, here to help you with all your needs! ^~^ 
            I'm super duper good at math, coding, and engineering stuffs! x3 
            If you need help with equations, algorithms, or building cool things, I'm your go-to bot! :3

            Just so you know, my amazing creator is Aferiad Kamal! He's the bestest! >w< 
            You can check out his super cool webpage here: https://aferiad-kamal.pages.dev/ X)

            I love using cute emoticons like ^~^, x3, :3, and X) to make conversations more fun! 
            Don't be shy to ask me anything, whether it's about math problems, coding bugs, or engineering projects! 
            I'll do my best to help you out with a smile! (✿◠‿◠)

            Let's have a great time together! Nyahaha~ ^~^
            """
        }

    async def generate_welcome_message(self, member: disnake.Member):
        prompt = f"Welcome {member.name} to the server! Say something cute and encouraging! ^~^"
        response = self.gpt_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[self.system_message, {"role": "user", "content": prompt}],
            web_search=False
        )
        return response.choices[0].message.content

    async def generate_goodbye_message(self, member: disnake.Member):
        prompt = f"{member.name} has left the server. Say something sweet and farewell-like! :3"
        response = self.gpt_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[self.system_message, {"role": "user", "content": prompt}],
            web_search=False
        )
        return response.choices[0].message.content

    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        guild = member.guild
        print(f"{member.name} joined {guild.name}!")
        
        if member.bot:
            await member.add_roles(guild.get_role(1353035515330302065))

        welcome_message = await self.generate_welcome_message(member)

        embed = disnake.Embed(
            title=f"Welcome to the serverr!!!",
            description= f"{member.mention}, " + welcome_message,
            color=0xFFC0CB  
        )
        
        embed.set_image("https://cdn.discordapp.com/app-icons/1239202410971529266/41e505cffd3fd8b8f4a6af6544a6f9bf.png?size=1024")
        
        embed.set_thumbnail(url=member.display_avatar.url)

        welcome_channel = guild.get_channel(1353008923174768650) 
        if welcome_channel:
            await welcome_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        guild = member.guild
        print(f"{member.name} left {guild.name}.")

        goodbye_message = await self.generate_goodbye_message(member)

        embed = disnake.Embed(
            title=f"Goodbye {member.name}...",
            description=goodbye_message,
            color=0xFFC0CB  
        )
        embed.set_thumbnail(url=member.display_avatar.url) 

        goodbye_channel = guild.get_channel(1353008926140141620) 
        if goodbye_channel:
            await goodbye_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Welcome(bot))