import random
from project.bots.bot import Bot, StrategyMeta
from project.game.bet import Bet
from typing import Optional, List, Tuple


class StrategicBot(Bot, metaclass=StrategyMeta):
    def __init__(self, name: str, budget: int):
        super().__init__(name, budget)
        self.initial_budget = budget
        self.history: List[
            Tuple[int, str]
        ] = []  # Stores the round history: (number, color)

    def update_history(self, number: int, color: str) -> None:
        """Adds the result of a round to the history."""
        self.history.append((number, color))
        # Keep only the last 5 rounds in history
        if len(self.history) > 5:
            self.history.pop(0)

    def determine_bet_color(self) -> str:
        """Determines the color for the next bet based on history."""
        if len(self.history) == 0:
            # First round: random bet
            return random.choice(["Red", "Black", "Green"])

        last_color = self.history[-1][1]
        if all(color != "Green" for _, color in self.history):
            # If green has not appeared in the last 5 rounds
            return "Green"

        # Bet on the opposite color of the last round
        if last_color == "Red":
            return "Black"
        elif last_color == "Black":
            return "Red"
        else:
            # If the last color was green, randomly choose between red and black
            return random.choice(["Red", "Black"])

    def place_bet(self) -> Optional[Bet]:
        # Determine the bet amount
        if self.budget <= self.initial_budget * 0.1:
            bet_amount = (
                self.budget
            )  # Bet all if the budget falls below 10% of the initial budget
        else:
            bet_amount = max(int(self.budget * 0.2), 1)  # Bet 20% of the current budget

        # Ensure the bet amount does not exceed the budget
        bet_amount = min(bet_amount, self.budget)

        bet_color = self.determine_bet_color()
        return Bet(amount=bet_amount, bet_type="color", choice=bet_color)
