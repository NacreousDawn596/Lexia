import json
import os

class Economy:
    def __init__(self):
        self.ECONOMY_FILE = "economy.json"
        self.load_economy_data()

    def load_economy_data(self):
        if not os.path.exists(self.ECONOMY_FILE):
            with open(self.ECONOMY_FILE, "w") as f:
                json.dump({}, f)
        with open(self.ECONOMY_FILE, "r") as f:
            self.economy_data = json.load(f)

    def save_economy_data(self):
        with open(self.ECONOMY_FILE, "w") as f:
            json.dump(self.economy_data, f, indent=4)

    def get_guild_economy(self, guild_id):
        if str(guild_id) not in self.economy_data:
            self.economy_data[str(guild_id)] = {}
        return self.economy_data[str(guild_id)]

    def get_user_balance(self, guild_id, user_id):
        economy = self.get_guild_economy(guild_id)
        return economy.get(str(user_id), 0)

    def add_coins_to_user(self, guild_id, user_id, amount):
        economy = self.get_guild_economy(guild_id)
        if str(user_id) not in economy:
            economy[str(user_id)] = 0
        economy[str(user_id)] += amount
        self.save_economy_data()