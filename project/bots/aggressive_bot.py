from project.bots.bot import Bot, StrategyMeta
from project.game.bet import Bet
from typing import Optional
import random


class AggressiveBot(Bot, metaclass=StrategyMeta):
    MAX_BUDGET_FOR_NUMBER_BET = 50
    NUMBER_BET_AMOUNT = 50
    MIN_BUDGET_FOR_COLOR_BET = 10
    COLOR_BET_AMOUNT = 10
    COLOR_CHOICE = "Black"
    MAX_NUMBER = 49

    def place_bet(self) -> Optional[Bet]:
        if self.budget >= self.MAX_BUDGET_FOR_NUMBER_BET:
            amount = min(self.NUMBER_BET_AMOUNT, self.budget)
            return Bet(
                amount=amount,
                bet_type="number",
                choice=random.randint(0, self.MAX_NUMBER),
            )
        elif self.budget >= self.MIN_BUDGET_FOR_COLOR_BET:
            amount = min(self.COLOR_BET_AMOUNT, self.budget)
            return Bet(amount=amount, bet_type="color", choice=self.COLOR_CHOICE)
        return None
