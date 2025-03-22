# gambling.py
import disnake
from disnake.ext import commands
from disnake.ui import Button, View
from typing import Dict, List, Optional
import random

class Card:
    def __init__(self, suit: str, rank: str):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank}{self.suit}"

    @property
    def value(self) -> int:
        if self.rank in ("J", "Q", "K"):
            return 10
        if self.rank == "A":
            return 11
        return int(self.rank)

class GameSession:
    def __init__(self, host: disnake.Member, game_type: str, bet: int):
        self.host = host
        self.game_type = game_type
        self.players = [host]
        self.bet = bet
        self.message: Optional[disnake.Message] = None
        self.started = False
        self.joinable = True
        self.pot = bet
        self.guild_id = host.guild.id

class BlackjackGame:
    def __init__(self, session: GameSession):
        self.session = session
        self.deck: List[Card] = []
        self.player_hands: Dict[int, List[Card]] = {}
        self.dealer_hand: List[Card] = []
        self.current_turn = 0
        self.game_over = False
        
        self.initialize_deck()
        self.deal_initial_cards()

    def initialize_deck(self):
        suits = ["♠", "♣", "♥", "♦"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.deck = [Card(s, r) for s in suits for r in ranks]
        random.shuffle(self.deck)

    def deal_initial_cards(self):
        for player in self.session.players:
            self.player_hands[player.id] = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]

    def calculate_hand_value(self, hand: List[Card]) -> int:
        value = sum(card.value for card in hand)
        aces = sum(1 for card in hand if card.rank == "A")
        
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1
        return value

class PokerGame:
    def __init__(self, session: GameSession):
        self.session = session
        self.deck: List[Card] = []
        self.player_hands: Dict[int, List[Card]] = {}
        self.community_cards: List[Card] = []
        self.pot = session.pot
        self.current_bets: Dict[int, int] = {}
        self.current_player_index = 0
        self.game_phase = 0  # 0: Pre-flop, 1: Flop, 2: Turn, 3: River
        self.initialize_deck()

    def initialize_deck(self):
        suits = ["♠", "♣", "♥", "♦"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.deck = [Card(s, r) for s in suits for r in ranks]
        random.shuffle(self.deck)

    def deal_private_cards(self):
        for player in self.session.players:
            self.player_hands[player.id] = [self.deck.pop(), self.deck.pop()]

    def deal_community_cards(self, num: int):
        self.community_cards.extend([self.deck.pop() for _ in range(num)])

class Gambling(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.active_sessions: Dict[int, GameSession] = {}
        self.active_games: Dict[int, PokerGame] = {}
        self.blackjack_games: Dict[int, BlackjackGame] = {}

    async def update_lobby_embed(self, session: GameSession):
        embed = disnake.Embed(
            title=f"{session.game_type.capitalize()} Lobby",
            description=f"Host: {session.host.mention}\nBet: {session.bet} coins",
            color=disnake.Color.green()
        )
        players_list = "\n".join([f"• {p.mention}" for p in session.players])
        embed.add_field(name=f"Players ({len(session.players)})", value=players_list, inline=False)
        embed.set_footer(text=f"Total Pot: {session.pot} coins")

        view = self.create_lobby_view(session)
        if session.message:
            await session.message.edit(embed=embed, view=view)

    def create_lobby_view(self, session: GameSession) -> View:
        view = View(timeout=None)
        view.add_item(Button(style=disnake.ButtonStyle.green, label="Join", custom_id=f"join_{session.host.id}"))
        view.add_item(Button(style=disnake.ButtonStyle.red, label="Leave", custom_id=f"leave_{session.host.id}"))
        view.add_item(Button(
            style=disnake.ButtonStyle.blurple, 
            label="Start Game", 
            custom_id=f"start_{session.host.id}", 
            disabled=not session.joinable
        ))
        return view

    @commands.slash_command(name="gamble", description="Start a gambling session")
    async def gamble(
        self,
        inter: disnake.ApplicationCommandInteraction,
        game: str = commands.Param(choices=["poker", "blackjack"]),
        bet: int = commands.Param(gt=0, description="Amount to bet")
    ):
        if not self.check_balance(inter.guild_id, inter.author.id, bet):
            return await inter.response.send_message(
                "You don't have enough coins to host this game!",
                ephemeral=True
            )

        session = GameSession(inter.author, game, bet, self.bot.economy)
        self.bot.economy.add_coins_to_user(inter.guild_id, inter.author.id, -bet)
        
        embed = disnake.Embed(
            title=f"{game.capitalize()} Lobby",
            description=f"Host: {inter.author.mention}\nBet: {bet} coins",
            color=disnake.Color.green()
        )
        view = self.create_lobby_view(session)
        
        await inter.response.send_message(embed=embed, view=view)
        session.message = await inter.original_message()
        self.active_sessions[session.message.id] = session

    def check_balance(self, guild_id: int, user_id: int, amount: int) -> bool:
        return self.bot.economy.get_user_balance(guild_id, user_id) >= amount

    @commands.Cog.listener()
    async def on_button_click(self, inter: disnake.MessageInteraction):
        if not inter.component.custom_id:
            return

        if inter.component.custom_id.startswith(("join_", "leave_", "start_")):
            session_id = inter.message.id
            session = self.active_sessions.get(session_id)
            
            if not session:
                await inter.response.send_message("This session has expired!", ephemeral=True)
                return

            action, host_id = inter.component.custom_id.split("_")
            host_id = int(host_id)

            if action == "join":
                await self.handle_join(inter, session)
            elif action == "leave":
                await self.handle_leave(inter, session)
            elif action == "start":
                await self.handle_start(inter, session)

        elif inter.component.custom_id.startswith(("bj_hit_", "bj_stand_")):
            await self.handle_blackjack_action(inter)

    async def handle_join(self, inter: disnake.MessageInteraction, session: GameSession):
        if inter.user == session.host:
            await inter.response.send_message("You're already the host!", ephemeral=True)
            return
        if inter.user in session.players:
            await inter.response.send_message("You're already in the game!", ephemeral=True)
            return
        if not self.check_balance(inter.guild_id, inter.user.id, session.bet):
            await inter.response.send_message("You can't afford to join this game!", ephemeral=True)
            return

        self.bot.economy.add_coins_to_user(inter.guild_id, inter.user.id, -session.bet)
        session.players.append(inter.user)
        session.pot += session.bet
        await self.update_lobby_embed(session)
        await inter.response.defer()

    async def handle_leave(self, inter: disnake.MessageInteraction, session: GameSession):
        if inter.user == session.host:
            await inter.response.send_message("Host can't leave! Cancel the game instead.", ephemeral=True)
            return
        if inter.user not in session.players:
            await inter.response.send_message("You're not in this game!", ephemeral=True)
            return

        self.bot.economy.add_coins_to_user(inter.guild_id, inter.user.id, session.bet)
        session.players.remove(inter.user)
        session.pot -= session.bet
        await self.update_lobby_embed(session)
        await inter.response.defer()

    async def handle_start(self, inter: disnake.MessageInteraction, session: GameSession):
        if inter.user != session.host:
            await inter.response.send_message("Only the host can start the game!", ephemeral=True)
            return
        if len(session.players) < 2:
            await inter.response.send_message("Need at least 2 players to start!", ephemeral=True)
            return

        session.joinable = False
        del self.active_sessions[session.message.id]

        if session.game_type == "blackjack":
            game = BlackjackGame(session)
            self.blackjack_games[session.message.channel.id] = game
            await self.start_blackjack(session, game)
        else:
            game = PokerGame(session)
            self.active_games[session.message.channel.id] = game
            await self.start_poker(session, game)

    async def start_blackjack(self, session: GameSession, game: BlackjackGame):
        for player in session.players:
            await player.send(
                "Your Blackjack hand: " + ", ".join(str(c) for c in game.player_hands[player.id]),
                ephemeral=True
            )

        embed = disnake.Embed(title="Blackjack Game", color=disnake.Color.blue())
        embed.add_field(
            name="Dealer's Hand",
            value=f"{str(game.dealer_hand[0])} 🂠",
            inline=False
        )
        embed.set_footer(text=f"Current turn: {session.players[0].display_name}")
        
        view = View()
        view.add_item(Button(style=disnake.ButtonStyle.green, label="Hit", custom_id=f"bj_hit_{session.host.id}"))
        view.add_item(Button(style=disnake.ButtonStyle.red, label="Stand", custom_id=f"bj_stand_{session.host.id}"))
        
        await session.message.channel.send(embed=embed, view=view)

    async def handle_blackjack_action(self, inter: disnake.MessageInteraction):
        channel_id = inter.channel.id
        game = self.blackjack_games.get(channel_id)
        if not game:
            return

        player = game.session.players[game.current_turn]
        if inter.user != player:
            await inter.response.send_message("It's not your turn!", ephemeral=True)
            return

        action = inter.component.custom_id.split("_")[1]
        if action == "hit":
            game.player_hands[player.id].append(game.deck.pop())
            hand_value = game.calculate_hand_value(game.player_hands[player.id])

            if hand_value > 21:
                await inter.channel.send(f"{player.mention} busts!")
                game.current_turn += 1
                if game.current_turn >= len(game.session.players):
                    await self.finish_blackjack(game)
                    return
            else:
                await inter.response.defer()
        else:
            game.current_turn += 1
            if game.current_turn >= len(game.session.players):
                await self.finish_blackjack(game)
                return

        await self.update_blackjack_embed(game, inter)

    async def finish_blackjack(self, game: BlackjackGame):
        dealer_value = game.calculate_hand_value(game.dealer_hand)
        while dealer_value < 17:
            game.dealer_hand.append(game.deck.pop())
            dealer_value = game.calculate_hand_value(game.dealer_hand)

        winners = []
        for player in game.session.players:
            player_value = game.calculate_hand_value(game.player_hands[player.id])
            if player_value > 21:
                continue
            if dealer_value > 21 or player_value > dealer_value:
                winners.append(player)

        if winners:
            payout = game.session.pot // len(winners)
            for winner in winners:
                self.bot.economy.add_coins_to_user(
                    game.session.guild_id,
                    winner.id,
                    payout
                )
            await game.session.message.channel.send(
                f"Dealer's hand: {', '.join(str(c) for c in game.dealer_hand)} ({dealer_value})\n"
                f"Winners: {', '.join(w.mention for w in winners)} - Each won {payout} coins!"
            )
        else:
            await game.session.message.channel.send("Dealer wins everyone loses!")

        del self.blackjack_games[game.session.message.channel.id]

    async def update_blackjack_embed(self, game: BlackjackGame, inter: disnake.MessageInteraction):
        embed = inter.message.embeds[0]
        embed.set_footer(text=f"Current turn: {game.session.players[game.current_turn].display_name}")
        await inter.message.edit(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Gambling(bot))