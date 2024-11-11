import random
from project.bots.bot import Bot
from project.game.bet import Bet
from typing import Optional, List, Tuple


class StrategicBot(Bot):
    """
    A strategic betting bot that determines bets based on historical outcomes.

    This bot analyzes the results of previous rounds to inform its betting strategy.
    It maintains a history of the last five rounds and adapts its betting color
    based on the observed patterns.

    Attributes:
        initial_budget (int): The initial budget when the bot was created.
        history (List[Tuple[int, str]]): A list storing the results of the last five rounds,
            with each entry containing a tuple of the number and color from the round.

    Methods:
        update_history(number: int, color: str) -> None:
            Records the result of a round in the history. If the history exceeds five entries,
            it removes the oldest entry.

        determine_bet_color() -> str:
            Determines the color for the next bet based on historical data. If there are no
            previous results, it randomly selects a color. If "Green" has not been chosen in
            the last five rounds, it will choose "Green". Otherwise, it alternates between "Red"
            and "Black" based on the last round's outcome.

        place_bet() -> Optional[Bet]:
            Calculates the amount to bet based on the current budget. If the budget is less than
            or equal to 10% of the initial budget, it bets all remaining funds. Otherwise, it bets
            20% of the current budget (or at least 1 unit). It then determines the color for the bet
            and returns a Bet object.
    """

    COLOR_GREEN: str = "Green"
    COLOR_RED: str = "Red"
    COLOR_BLACK: str = "Black"
    BET_TYPE_COLOR: str = "color"

    def __init__(self, name: str, budget: int):
        super().__init__(name, budget)
        self.initial_budget = budget
        self.history: List[Tuple[int, str]] = []

    def update_history(self, number: int, color: str) -> None:
        """Adds the result of a round to the history."""
        self.history.append((number, color))
        if len(self.history) > 5:
            self.history.pop(0)

    def determine_bet_color(self) -> str:
        """Determines the color for the next bet based on history."""
        if len(self.history) == 0:
            return random.choice(["Red", "Black", "Green"])

        last_color = self.history[-1][1]
        if all(color != self.COLOR_GREEN for _, color in self.history):
            return self.COLOR_GREEN

        if last_color == self.COLOR_RED:
            return self.COLOR_BLACK
        elif last_color == self.COLOR_BLACK:
            return self.COLOR_RED
        else:
            return random.choice(["Red", "Black"])

    def place_bet(self) -> Optional[Bet]:
        if self.budget <= self.initial_budget * 0.1:
            bet_amount = self.budget
        else:
            bet_amount = max(int(self.budget * 0.2), 1)

        bet_amount = min(bet_amount, self.budget)

        bet_color = self.determine_bet_color()
        return Bet(amount=bet_amount, bet_type=self.BET_TYPE_COLOR, choice=bet_color)
