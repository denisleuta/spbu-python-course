from project.bots.bot import Bot
from project.game.bet import Bet
from typing import Optional
import random


class AggressiveBot(Bot):
    def place_bet(self) -> Optional[Bet]:
        if self.budget >= 50:
            return Bet(amount=50, bet_type="number", choice=random.randint(0, 49))
        elif self.budget >= 10:
            return Bet(amount=10, bet_type="color", choice="Black")
        return None
