from project.bots.bot import Bot
from project.game.bet import Bet
from typing import Optional
import random


class RandomBot(Bot):
    def place_bet(self) -> Optional[Bet]:
        if self.budget > 0:
            amount = random.randint(
                1, min(20, self.budget)
            )  # Случайная сумма, ограниченная бюджетом
            bet_type = random.choice(["color", "number"])
            if bet_type == "color":
                choice = random.choice(["Red", "Black", "Green"])
            else:
                choice = random.randint(0, 49)  # Ставка на случайное число
            return Bet(amount=amount, bet_type=bet_type, choice=choice)
        return None
