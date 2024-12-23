from project.bots.bot import Bot
from project.game.bet import Bet
from typing import Optional
import random


class AggressiveBot(Bot):
    """
    An aggressive betting strategy bot that places bets on a game.

    This bot prioritizes placing bets on numbers when the budget allows,
    and resorts to color bets when the budget is insufficient for number bets.

    Attributes:
        MAX_BUDGET_FOR_NUMBER_BET (int): The maximum budget allowed for placing a number bet.
        NUMBER_BET_AMOUNT (int): The fixed amount to bet on a number.
        MIN_BUDGET_FOR_COLOR_BET (int): The minimum budget required to place a color bet.
        COLOR_BET_AMOUNT (int): The fixed amount to bet on a color.
        COLOR_CHOICE (str): The color choice for color bets (default is "Black").
        MAX_NUMBER (int): The maximum number that can be chosen for number bets.

    Methods:
        place_bet() -> Optional[Bet]:
            Places a bet based on the current budget. If the budget is sufficient,
            it places a number bet; otherwise, it places a color bet if the budget
            allows. Returns a Bet object if a bet is placed, or None if no bet can be made.
    """

    MAX_BUDGET_FOR_NUMBER_BET: int = 50
    NUMBER_BET_AMOUNT: int = 50
    MIN_BUDGET_FOR_COLOR_BET: int = 10
    COLOR_BET_AMOUNT: int = 10
    COLOR_CHOICE: str = "Black"
    MAX_NUMBER: int = 49
    BET_TYPE_NUMBER: str = "number"
    BET_TYPE_COLOR: str = "color"

    def place_bet(self) -> Optional[Bet]:
        if self.budget >= self.MAX_BUDGET_FOR_NUMBER_BET:
            amount = min(self.NUMBER_BET_AMOUNT, self.budget)
            return Bet(
                amount=amount,
                bet_type=self.BET_TYPE_NUMBER,
                choice=random.randint(0, self.MAX_NUMBER),
            )
        elif self.budget >= self.MIN_BUDGET_FOR_COLOR_BET:
            amount = min(self.COLOR_BET_AMOUNT, self.budget)
            return Bet(
                amount=amount, bet_type=self.BET_TYPE_COLOR, choice=self.COLOR_CHOICE
            )
        return None
