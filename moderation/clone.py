import disnake
from disnake.ext import commands
import aiohttp, asyncio

class ServerClone(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="clone", description="copy a server A into a server B lol")
    @commands.has_guild_permissions(administrator=True)
    async def clone_guild(
        self,
        inter: disnake.ApplicationCommandInteraction,
        source_guild_id: str
    ):
        await inter.response.defer()
        
        target_guild = inter.guild
        try:
            source_guild = await self.bot.fetch_guild(int(source_guild_id))
        except disnake.NotFound:
            return await inter.edit_original_message("Source guild not found")

        for channel in target_guild.channels:
            if "rule" not in channel.name and "moderator" not in channel.name:
                await channel.delete(reason="Preparing for server clone")
                await asyncio.sleep(1)
        await self.copy_guild_settings(source_guild, target_guild)
        
        role_mapping = await self.clone_roles(source_guild, target_guild)
        
        await self.clone_channels(source_guild, target_guild, role_mapping)
        
        await self.clone_emojis(source_guild, target_guild)
        await self.clone_stickers(source_guild, target_guild)

        await inter.edit_original_message("Server cloning complete!")

    async def copy_guild_settings(self, source, target):
        await target.edit(
            name=f"{source.name} [CLONE]",
            icon=await source.icon.read() if source.icon else None,
            verification_level=source.verification_level,
        )

    async def clone_roles(self, source, target):
        role_mapping = {}
        roles = sorted(await source.fetch_roles(), key=lambda r: -r.position)
        
        for role in roles:
            if role.is_default() or role.managed:
                continue  
                
            new_role = await target.create_role(
                name=role.name,
                permissions=role.permissions,
                color=role.color,
                hoist=role.hoist,
                mentionable=role.mentionable
            )
            role_mapping[role.id] = new_role.id
            
        return role_mapping

    async def clone_channels(self, source, target, role_mapping):
        source_role_names = {role.name for role in source.roles}
        for role in target.roles:
            if role.is_default() or role.managed:
                continue
            if role.name not in source_role_names:
                await role.delete(reason="Preparing for server clone")
                await asyncio.sleep(1)

        categories = [c for c in await source.fetch_channels() if isinstance(c, disnake.CategoryChannel)]
        category_mapping = {}
        
        for category in categories:
            overwrites = self.convert_overwrites(category.overwrites, role_mapping)
            new_category = await target.create_category_channel(
                name=category.name,
                overwrites=overwrites,
                position=category.position
            )
            category_mapping[category.id] = new_category

        channels = [c for c in await source.fetch_channels() if not isinstance(c, disnake.CategoryChannel)]
        
        for channel in channels:
            overwrites = self.convert_overwrites(channel.overwrites, role_mapping)
            parent = category_mapping.get(channel.category_id)
            
            if isinstance(channel, disnake.TextChannel):
                await target.create_text_channel(
                    name=channel.name,
                    topic=channel.topic,
                    position=channel.position,
                    nsfw=channel.nsfw,
                    slowmode_delay=channel.slowmode_delay,
                    category=parent,
                    overwrites=overwrites
                )
            elif isinstance(channel, disnake.VoiceChannel):
                await target.create_voice_channel(
                    name=channel.name,
                    position=channel.position,
                    bitrate=channel.bitrate,
                    user_limit=channel.user_limit,
                    category=parent,
                    overwrites=overwrites
                )

    def convert_overwrites(self, overwrites, role_mapping):
        new_overwrites = {}
        for target, overwrite in overwrites.items():
            if isinstance(target, disnake.Role):
                if target.id in role_mapping:
                    new_target = target.guild.get_role(role_mapping[target.id])
                    if new_target:
                        new_overwrites[new_target] = overwrite
        return new_overwrites

    async def clone_emojis(self, source, target):
        async with aiohttp.ClientSession() as session:
            for emoji in await source.fetch_emojis():
                async with session.get(str(emoji.url)) as resp:
                    image = await resp.read()
                    await target.create_custom_emoji(
                        name=emoji.name,
                        image=image,
                        reason="Server cloning"
                    )

    async def clone_stickers(self, source, target):
        for sticker in await source.fetch_stickers():
            async with aiohttp.ClientSession() as session:
                async with session.get(str(sticker.url)) as resp:
                    sticker_image = await resp.read()
                    await target.create_sticker(
                        name=sticker.name,
                        description=sticker.description,
                        emoji=sticker.emoji,
                        file=disnake.File(sticker_image, filename=sticker.image_url.split("/")[-1]),
                        reason="Server cloning"
                    )

def setup(bot):
    bot.add_cog(ServerClone(bot))
