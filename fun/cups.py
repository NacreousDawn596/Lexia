# cups.py
import disnake
from disnake.ext import commands
from disnake.ui import Button, View
import random
from typing import Dict, List, Optional

class CupsGame:
    def __init__(self, host: disnake.Member, word_length: int, max_guesses: int):
        self.host = host
        self.players = [host]
        self.word_length = word_length
        self.max_guesses = max_guesses
        self.word = self.generate_word().upper()
        self.guesses: List[str] = []
        self.revealed = ['_'] * word_length
        self.remaining_guesses = max_guesses
        self.message: Optional[disnake.Message] = None
        self.started = False
        self.channel_id: Optional[int] = None

    def generate_word(self) -> str:
        word_bank = {
            3: ['CAT', 'DOG', 'SUN', 'CAR', 'PEN', 'HAT', 'BAG', 'LEG', 'EYE', 'ARM', 
                'ICE', 'JOB', 'KEY', 'LAP', 'MAP', 'NET', 'OAK', 'PIE', 'RAT', 'SEA', 
                'TEA', 'URN', 'VAN', 'WAX', 'YES', 'ZIP', 'ACT', 'ADD', 'AGE', 'AIR', 
                'ANT', 'APE', 'ART', 'ASH', 'AWE', 'BAD', 'BAR', 'BAT', 'BED', 'BEE', 
                'BET', 'BIN', 'BIT', 'BOX', 'BOY', 'BUS', 'BUT', 'BUY', 'BYE', 'CAB'],
            
            4: ['LOVE', 'HATE', 'DOOR', 'WIND', 'FISH', 'BIRD', 'TREE', 'CAKE', 'FIRE', 
                'BEAR', 'SOUP', 'SNOW', 'BOOK', 'BALL', 'HAND', 'FOOT', 'HAIR', 'FACE', 
                'NOSE', 'EARS', 'LION', 'WOLF', 'FROG', 'DUCK', 'MOON', 'STAR', 'LAKE', 
                'ROAD', 'SHIP', 'COAT', 'SHOE', 'DESK', 'LAMP', 'BOWL', 'FORK', 'KNIFE', 
                'PLATE', 'CUP', 'BOTTLE', 'CHAIR', 'TABLE', 'SOFA', 'BED', 'WALL', 
                'DOOR', 'WINDOW', 'CLOUD', 'GRASS', 'FLOWER', 'SAND'],
            
            5: ['APPLE', 'BEACH', 'CLOUD', 'DRINK', 'EAGLE', 'FRUIT', 'GHOST', 'HONEY', 
                'HOUSE', 'JUICE', 'KNIFE', 'LEMON', 'MONEY', 'NIGHT', 'OCEAN', 'PARTY', 
                'QUEEN', 'RIVER', 'SNAKE', 'TABLE', 'UMBRA', 'VITAL', 'WATCH', 'YACHT', 
                'ZEBRA', 'BRAIN', 'CHAIR', 'DANCE', 'EARTH', 'FROST', 'GRAPE', 'HORSE', 
                'IGLOO', 'JELLY', 'KOALA', 'LIGHT', 'MAGIC', 'NINJA', 'OLIVE', 'PEARL', 
                'QUILT', 'ROBOT', 'SHEEP', 'TIGER', 'UNION', 'VIOLA', 'WHALE', 'XENON', 
                'YACHT', 'ZEBRA'],
            
            6: ['BANANA', 'CASTLE', 'DRAGON', 'FLOWER', 'GARDEN', 'JUNGLE', 'KETTLE', 
                'MONKEY', 'ORANGE', 'PURPLE', 'RABBIT', 'SPHERE', 'TIGER', 'TURTLE', 
                'WINDOW', 'YELLOW', 'ANCHOR', 'BRIDGE', 'CANDLE', 'DINNER', 'ELEPHANT', 
                'FAMILY', 'GINGER', 'HARBOR', 'ISLAND', 'JACKET', 'KITTEN', 'LADDER', 
                'MIRROR', 'NATURE', 'OXYGEN', 'PENCIL', 'QUARTZ', 'ROCKET', 'SILVER', 
                'TEMPLE', 'UNICORN', 'VIOLIN', 'WAGON', 'YOGURT', 'ZODIAC', 'ALMOND', 
                'BASKET', 'CIRCLE', 'DOLPHIN', 'EAGLET', 'FALCON', 'GARLIC', 'HICKORY', 
                'INSECT'],
            
            7: ['BALLOON', 'CABINET', 'DIAMOND', 'ELECTRIC', 'FACTORY', 'GIRAFFE', 
                'HAMBURG', 'ICEBERG', 'JACKET', 'KANGAROO', 'LIBRARY', 'MEDICAL', 
                'NATURAL', 'OCTOPUS', 'PENGUIN', 'QUALITY', 'RAINBOW', 'SUNSHINE', 
                'TRAFFIC', 'UMBRELLA', 'VICTORY', 'WALRUS', 'XYLOPHONE', 'YELLOW', 
                'ZEBRAS', 'ACROBAT', 'BICYCLE', 'CACTUS', 'DOLPHIN', 'ECLIPSE', 
                'FIREFLY', 'GALAXY', 'HARMONY', 'ICICLE', 'JOURNEY', 'KITTENS', 
                'LIGHTER', 'MAGNET', 'NESTING', 'ORCHARD', 'PACKAGE', 'QUARTET', 
                'RACCOON', 'SANDWICH', 'TELESCOPE', 'UNICORN', 'VAMPIRE', 'WIZARD', 
                'XENON', 'YOGURT'],
            
            8: ['AIRPLANE', 'BASEBALL', 'COMPUTER', 'ELEPHANT', 'HOSPITAL', 'INTERNET', 
                'MOUNTAIN', 'NOTEBOOK', 'PASSWORD', 'QUESTION', 'RAINCOAT', 'SUNGLASS', 
                'TELEVISION', 'UNIVERSITY', 'VACATION', 'WATERFALL', 'BIRTHDAY', 
                'CAMERA', 'DINOSAUR', 'ELEVATOR', 'FIREWORK', 'GOLDFISH', 'HAMBURGER', 
                'ISLANDER', 'JELLYBEAN', 'KEYBOARD', 'LIGHTHOUSE', 'MOTORCYCLE', 
                'NOTEBOOK', 'OCTAGON', 'PINEAPPLE', 'QUARTZ', 'RAINBOW', 'SANDWICH', 
                'TELEPHONE', 'UMBRELLA', 'VANILLA', 'WATERMELON', 'XYLOPHONE', 
                'YELLOWSTONE', 'ZUCCHINI', 'ALPHABET', 'BROWNIE', 'CUPCAKE', 'DOLPHIN', 
                'ELEPHANT', 'FIREFLY', 'GARDEN', 'HONEYDEW', 'ICECREAM'],
            
            9: ['ADVENTURE', 'BUTTERFLY', 'CHOCOLATE', 'DANGEROUS', 'EDUCATION', 
                'FIREPLACE', 'GRATITUDE', 'HURRICANE', 'INSURANCE', 'JELLYFISH', 
                'KILOMETER', 'LIGHTNING', 'MICROSCOPE', 'NOTEBOOKS', 'OPERATION', 
                'PINEAPPLE', 'QUALIFIED', 'RESTAURANT', 'SANDWICHES', 'TELEPHONE', 
                'UNIVERSE', 'VEGETABLE', 'WAREHOUSE', 'XYLOPHONE', 'YESTERDAY', 
                'ZUCCHINI', 'AIRCRAFT', 'BASKETBALL', 'CINNAMON', 'DETECTIVE', 
                'ELEPHANT', 'FIREWORKS', 'GARDENING', 'HAMBURGER', 'INSTRUMENT', 
                'JELLYBEAN', 'KANGAROO', 'LIGHTHOUSE', 'MAGNOLIA', 'NOTEBOOK', 
                'OCTOPUS', 'PASSENGER', 'QUARTERBACK', 'RAINBOW', 'SUNFLOWER', 
                'TELEVISION', 'UMBRELLA', 'VANILLA', 'WATERMELON', 'YELLOWSTONE'],
            
            10: ['BLACKBOARD', 'STRAWBERRY', 'CHOCOLATES', 'DICTIONARY', 'ELECTRICITY', 
                'FLASHLIGHT', 'GRAPEFRUIT', 'HYPOTHESIS', 'INSTRUMENT', 'JOURNALIST', 
                'KEYBOARD', 'LIGHTHOUSE', 'METROPOLIS', 'NOTEBOOK', 'OSTRICHES', 
                'PHOTOGRAPH', 'QUARTERBACK', 'REFRIGERATOR', 'SUNSCREEN', 'TELEVISION', 
                'UNDERGROUND', 'VIOLINIST', 'WATERMELON', 'XYLOPHONES', 'YELLOWSTONE', 
                'ZIGZAGGING', 'AEROPLANE', 'BASKETBALL', 'CATERPILLAR', 'DETECTIVE', 
                'ELEPHANT', 'FIREWORKS', 'GARDENING', 'HAMBURGER', 'INSTRUMENT', 
                'JELLYBEAN', 'KANGAROO', 'LIGHTHOUSE', 'MAGNOLIA', 'NOTEBOOK', 
                'OCTOPUS', 'PASSENGER', 'QUARTERBACK', 'RAINBOW', 'SUNFLOWER', 
                'TELEVISION', 'UMBRELLA', 'VANILLA', 'WATERMELON', 'YELLOWSTONE'],
            
            11: ['CELEBRATION', 'COMMUNICATION', 'DESTRUCTION', 'ENVIRONMENT', 
                'FLUORESCENT', 'GRANDCHILDREN', 'HIBERNATION', 'ILLUMINATION', 
                'JUGGERNAUTS', 'KINDERGARTEN', 'LUMBERJACKS', 'MAGNIFICENT', 
                'NATIONALISM', 'OPPORTUNITY', 'PHILOSOPHY', 'QUESTIONING', 
                'REFLECTIONS', 'SPECTACULAR', 'TRANSPORTATION', 'UNDERWEAR', 
                'VEGETARIAN', 'WHISTLEBLOWER', 'XENOPHOBIA', 'YELLOWTHROAT', 
                'ZOOPLANKTON', 'ASTRONAUTICAL', 'BIBLIOGRAPHY', 'CATASTROPHIC', 
                'DEMOCRATICAL', 'ELECTROCUTION', 'FOUNDATIONAL', 'GENEALOGICAL', 
                'HYPOTHETICAL', 'ILLUSTRATION', 'JURISDICTION', 'KALEIDOSCOPE', 
                'LIGHTHOUSES', 'METAPHYSICAL', 'NEUROSCIENCE', 'OMNIPRESENT', 
                'PHOTOGRAPHIC', 'QUINTESSENTIAL', 'REVOLUTIONARY', 'SYMPHONICALLY', 
                'TELECOMMUTING', 'UNDERSTANDING', 'VEGETATION', 'WATERPROOF', 
                'XENOPHOBIA', 'YELLOWSTONE'],
            
            12: ['ASTRONAUTICAL', 'BIBLIOGRAPHY', 'CATASTROPHIC', 'DEMOCRATICAL', 
                'ELECTROCUTION', 'FOUNDATIONAL', 'GENEALOGICAL', 'HYPOTHETICAL', 
                'ILLUSTRATION', 'JURISDICTION', 'KALEIDOSCOPE', 'LIGHTHOUSES', 
                'METAPHYSICAL', 'NEUROSCIENCE', 'OMNIPRESENT', 'PHOTOGRAPHIC', 
                'QUINTESSENTIAL', 'REVOLUTIONARY', 'SYMPHONICALLY', 'TELECOMMUTING', 
                'UNDERSTANDING', 'VEGETATION', 'WATERPROOF', 'XENOPHOBIC', 
                'YELLOWSTONE', 'AERODYNAMICS', 'BIOGRAPHICAL', 'CATASTROPHE', 
                'DEMOCRATIC', 'ELECTRICITY', 'FOUNDATION', 'GENEALOGY', 'HYPOTHESIS', 
                'ILLUMINATE', 'JURISDICTIONAL', 'KALEIDOSCOPIC', 'LIGHTNING', 
                'METAPHORICAL', 'NEUROLOGICAL', 'OMNIPOTENT', 'PHOTOGRAPHY', 
                'QUINTESSENCE', 'REVOLUTION', 'SYMPHONY', 'TELECOMMUTE', 
                'UNDERSTAND', 'VEGETARIAN', 'WATERFALL', 'XENOPHOBIC', 'YELLOWSTONE']
        }
        return random.choice(word_bank.get(self.word_length, ["PYTHON"]))

    def process_guess(self, guess: str) -> bool:
        guess = guess.upper()
        self.guesses.append(guess)
        self.remaining_guesses -= 1
        
        # Update revealed letters
        new_revealed = list(self.revealed)
        for i in range(min(len(guess), self.word_length)):
            if guess[i] == self.word[i]:
                new_revealed[i] = guess[i]
        self.revealed = new_revealed
        
        return self.word == ''.join(self.revealed)

    @property
    def display_status(self) -> str:
        return ' '.join(self.revealed)

class Cups(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.active_games: Dict[int, CupsGame] = {}  # {channel_id: game}

    @commands.slash_command(name="cups")
    async def cups(self, inter: disnake.ApplicationCommandInteraction):
        pass

    @cups.sub_command(name="start", description="Start a new cups game session")
    async def cups_start(
        self,
        inter: disnake.ApplicationCommandInteraction,
        length: int = commands.Param(ge=4, le=8, description="Word length (4-8)"),
        guesses: int = commands.Param(ge=3, le=15, description="Number of allowed guesses (3-15)")
    ):
        if inter.channel.id in self.active_games:
            return await inter.response.send_message(
                "A game is already running in this channel!", 
                ephemeral=True
            )

        game = CupsGame(inter.author, length, guesses)
        game.channel_id = inter.channel.id
        self.active_games[inter.channel.id] = game
        
        embed = self.create_lobby_embed(game)
        view = self.create_lobby_buttons(game)
        
        await inter.response.send_message(embed=embed, view=view)
        game.message = await inter.original_message()

    def create_lobby_embed(self, game: CupsGame) -> disnake.Embed:
        embed = disnake.Embed(
            title="🎮 Cups Game Lobby",
            color=disnake.Color.blue()
        )
        embed.add_field(
            name="Game Settings",
            value=f"**Word Length:** {game.word_length}\n**Max Guesses:** {game.max_guesses}",
            inline=False
        )
        embed.add_field(
            name="Players",
            value='\n'.join([p.mention for p in game.players]) or "No players yet",
            inline=False
        )
        embed.set_footer(text=f"Hosted by {game.host.display_name}")
        return embed

    def create_lobby_buttons(self, game: CupsGame) -> View:
        view = View(timeout=None)
        view.add_item(Button(style=disnake.ButtonStyle.green, label="Join", custom_id=f"cups_join_{game.host.id}"))
        view.add_item(Button(style=disnake.ButtonStyle.red, label="Leave", custom_id=f"cups_leave_{game.host.id}"))
        view.add_item(Button(style=disnake.ButtonStyle.blurple, label="Start", custom_id=f"cups_start_{game.host.id}"))
        return view

    @commands.slash_command(name="cup")
    async def cup(self, inter: disnake.ApplicationCommandInteraction):
        pass

    @cup.sub_command(name="guess", description="Make a word guess")
    async def cup_guess(
        self,
        inter: disnake.ApplicationCommandInteraction,
        word: str = commands.Param(description="Your guessed word (letters only)")
    ):
        game = self.active_games.get(inter.channel_id)
        
        if not game:
            return await inter.response.send_message(
                "No active game in this channel!", 
                ephemeral=True
            )
            
        if not game.started:
            return await inter.response.send_message(
                "Game hasn't started yet!", 
                ephemeral=True
            )
            
        if inter.user not in game.players:
            return await inter.response.send_message(
                "You're not in this game!", 
                ephemeral=True
            )

        # Validation
        if len(word) != game.word_length:
            return await inter.response.send_message(
                f"Word must be {game.word_length} characters long!", 
                ephemeral=True
            )
            
        if not word.isalpha():
            return await inter.response.send_message(
                "Only letters are allowed!", 
                ephemeral=True
            )
            
        if word.upper() in [g.upper() for g in game.guesses]:
            return await inter.response.send_message(
                "Already guessed this word!", 
                ephemeral=True
            )

        # Process guess
        won = game.process_guess(word)
        embed = disnake.Embed(
            title=f"Guess #{len(game.guesses)}/{game.max_guesses}",
            description=f"```\n{game.display_status}\n```",
            color=disnake.Color.green() if won else disnake.Color.orange()
        )
        embed.add_field(name="Your Guess", value=word.upper(), inline=False)
        
        if won:
            embed.title = "🎉 Correct! Game Won!"
            embed.description = f"The word was: **{game.word}**"
            embed.color = disnake.Color.gold()
            del self.active_games[inter.channel_id]
        elif game.remaining_guesses <= 0:
            embed.title = "💀 Game Over! No Guesses Left"
            embed.description = f"The word was: **{game.word}**"
            embed.color = disnake.Color.red()
            del self.active_games[inter.channel_id]
        
        await inter.response.send_message(embed=embed)

    @commands.Cog.listener()
    async def on_button_click(self, inter: disnake.MessageInteraction):
        if not inter.component.custom_id.startswith("cups_"):
            return
            
        _, action, host_id = inter.component.custom_id.split("_")
        host_id = int(host_id)
        game = next((g for g in self.active_games.values() if g.host.id == host_id), None)

        if not game:
            await inter.response.send_message("Game session expired!", ephemeral=True)
            return

        if action == "join":
            await self.handle_join(inter, game)
        elif action == "leave":
            await self.handle_leave(inter, game)
        elif action == "start":
            await self.handle_start(inter, game)

    async def handle_join(self, inter: disnake.MessageInteraction, game: CupsGame):
        if inter.user in game.players:
            await inter.response.send_message("You're already in the game!", ephemeral=True)
            return
            
        game.players.append(inter.user)
        await self.update_lobby(game)
        await inter.response.defer()

    async def handle_leave(self, inter: disnake.MessageInteraction, game: CupsGame):
        if inter.user == game.host:
            await inter.response.send_message("Host can't leave! Cancel the game instead.", ephemeral=True)
            return
            
        if inter.user in game.players:
            game.players.remove(inter.user)
            await self.update_lobby(game)
            await inter.response.defer()

    async def handle_start(self, inter: disnake.MessageInteraction, game: CupsGame):
        if inter.user != game.host:
            await inter.response.send_message("Only the host can start the game!", ephemeral=True)
            return
            
        if len(game.players) < 1:
            await inter.response.send_message("Need at least 1 player to start!", ephemeral=True)
            return

        game.started = True
        await self.update_lobby(game)
        await inter.channel.send(
            embed=disnake.Embed(
                title="🔤 Game Started!",
                description=(
                    f"**Word Length:** {game.word_length}\n"
                    f"**Guesses Remaining:** {game.max_guesses}\n\n"
                    "Use `/cup guess <word>` to make guesses!"
                ),
                color=disnake.Color.green()
            )
        )

    async def update_lobby(self, game: CupsGame):
        embed = self.create_lobby_embed(game)
        await game.message.edit(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Cups(bot))