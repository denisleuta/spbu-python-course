from project.bots.bot import Bot, StrategyMeta
from project.game.bet import Bet
from typing import Optional


class OnlyGreenBot(Bot, metaclass=StrategyMeta):
    """
    A betting bot that exclusively places bets on the color green.

    This bot is designed to place color bets only when the budget allows it.
    It will always choose green as its betting color.

    Attributes:
        BET_AMOUNT (int): The fixed amount to bet on the color green.
        COLOR_BET_TYPE (str): The type of bet being placed (always "color").
        COLOR_CHOICE (str): The specific color choice for betting (always "Green").
        MIN_BUDGET_FOR_BET (int): The minimum budget required to place a bet.

    Methods:
        place_bet() -> Optional[Bet]:
            Places a bet on the color green if the current budget meets the minimum requirement.
            Returns a Bet object if a bet is placed, or None if the budget is insufficient.
    """
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
