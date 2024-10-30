from project.bots.bot import Bot, StrategyMeta
from project.game.bet import Bet
from typing import Optional


class OnlyGreenBot(Bot, metaclass=StrategyMeta):
    BET_AMOUNT = 10
    COLOR_BET_TYPE = "color"
    COLOR_CHOICE = "Green"
    MIN_BUDGET_FOR_BET = 10

    def place_bet(self) -> Optional[Bet]:
        if self.budget >= self.MIN_BUDGET_FOR_BET:
            amount = min(self.BET_AMOUNT, self.budget)
            return Bet(
                amount=amount, bet_type=self.COLOR_BET_TYPE, choice=self.COLOR_CHOICE
            )
        return None
