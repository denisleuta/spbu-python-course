import random
from typing import List, Optional, Tuple, Union


class StrategyMeta(type):
    """
    Metaclass for registering different bot strategies dynamically.
    """

    strategies: dict[str, type] = {}

    def __new__(cls, name, bases, dct):
        new_cls = super().__new__(cls, name, bases, dct)
        if name != "Bot":
            StrategyMeta.strategies[name] = new_cls
        return new_cls


class GameRuleMeta(type):
    """
    Metaclass for configuring game rules dynamically, such as fields and victory conditions.
    """

    def __new__(cls, name, bases, dct):
        dct["NUMBER_OF_FIELDS"] = 50
        dct["WINNING_BUDGET"] = 1000
        return super().__new__(cls, name, bases, dct)


class Bet:
    """
    Represents a bet placed by a bot in the game of Roulette.

    Attributes:
        amount (int): The amount of money bet.
        bet_type (str): The type of bet (e.g., 'color' or 'number').
        choice (int | str): The choice made for the bet, either a color or a specific number.
    """

    def __init__(self, amount: int, bet_type: str, choice: Union[int | str]) -> None:
        self.amount = amount
        self.bet_type = bet_type
        self.choice = choice


class Bot(metaclass=StrategyMeta):
    """
    Base class for bots, with a dynamic strategy registration via StrategyMeta.
    """

    def __init__(self, name: str, budget: int) -> None:
        self.name = name
        self.budget = budget

    def place_bet(self) -> Optional[Bet]:
        pass

    def update_budget(self, amount: int) -> None:
        self.budget += amount


class ConservativeBot(Bot):
    """
    A bot with a conservative betting strategy, always betting on red with a fixed amount.
    """

    def place_bet(self) -> Optional[Bet]:
        if self.budget > 0:
            return Bet(amount=10, bet_type="color", choice="Red")
        return None


class AggressiveBot(Bot):
    """
    A bot with an aggressive betting strategy, betting a large amount on a specific number.
    """

    def place_bet(self) -> Optional[Bet]:
        if self.budget > 0:
            number_choice = random.randint(1, 36)
            return Bet(amount=50, bet_type="number", choice=number_choice)
        return None


class RandomBot(Bot):
    """
    A bot with a random betting strategy, choosing randomly between color and number bets.
    """

    def place_bet(self) -> Optional[Bet]:
        if self.budget > 0:
            bet_type = random.choice(["color", "number"])
            if bet_type == "color":
                color_choice = random.choice(["Red", "Black"])
                return Bet(amount=20, bet_type="color", choice=color_choice)
            else:
                number_choice = random.randint(0, 36)
                return Bet(amount=20, bet_type="number", choice=number_choice)
        return None


class OnlyGreenBot(Bot):
    """
    A bot with a risky betting strategy, betting on the rarest 'Green' color.
    """

    def place_bet(self) -> Optional[Bet]:
        if self.budget > 0:
            return Bet(amount=20, bet_type="color", choice="Green")
        return None


class RouletteGame(metaclass=GameRuleMeta):
    """
    Represents the game of Roulette, managing the bots, rounds, and game mechanics.

    Attributes:
        bots (List[Bot]): The list of bots participating in the game.
        round (int): The current round number.
        max_steps (int): The maximum number of rounds to play.
    """

    COLORS = ["Red", "Black", "Green"]
    NUMBER_OF_FIELDS: int
    WINNING_BUDGET: int

    def __init__(self, bots: List[Bot], max_steps: int = 10) -> None:
        self.bots = bots
        self.round = 1
        self.max_steps = max_steps

    def spin_wheel(self) -> Tuple[int, str]:
        """
        Spins the roulette wheel and determines the outcome.

        Returns:
            Tuple[int, str]: A tuple containing the result number and its associated color.
        """
        result_number = random.randint(0, self.NUMBER_OF_FIELDS - 1)
        result_color = (
            "Green"
            if result_number == 0
            else "Red"
            if result_number % 2 == 0
            else "Black"
        )
        return result_number, result_color

    def evaluate_bets(self, bet: Bet, result_number: int, result_color: str) -> int:
        """
        Evaluates the outcome of a bet based on the result of the spin.

        Args:
            bet (Bet): The bet to evaluate.
            result_number (int): The number that was spun on the roulette wheel.
            result_color (str): The color that was spun on the roulette wheel.

        Returns:
            int: The amount won or lost based on the bet outcome.
        """
        if bet.bet_type == "color" and bet.choice == result_color:
            return bet.amount * (35 if result_color == "Green" else 2)
        elif bet.bet_type == "number" and bet.choice == result_number:
            return bet.amount * 36
        return -bet.amount

    def display_state(self) -> None:
        """
        Displays the current state of the game, including the round number and each bot's budget.
        """
        print(f"Round {self.round}:")
        for bot in self.bots:
            print(f"  {bot.name} budget: {bot.budget}")
        print("-" * 30)

    def play_round(self) -> None:
        """
        Plays a single round of the roulette game, spinning the wheel and processing bets.
        """
        result_number, result_color = self.spin_wheel()
        print(f"Roulette spun to {result_number} ({result_color})")

        for bot in self.bots:
            bet = bot.place_bet()
            if bet:
                outcome = self.evaluate_bets(bet, result_number, result_color)
                bot.update_budget(outcome)
                print(
                    f"{bot.name} bet {bet.amount} on {bet.choice} ({bet.bet_type}) and {'won' if outcome > 0 else 'lost'} {abs(outcome)}"
                )

        self.display_state()
        self.round += 1

    def check_for_winner(self) -> Optional[Bot]:
        for bot in self.bots:
            if bot.budget >= self.WINNING_BUDGET:
                return bot

        active_bots = [bot for bot in self.bots if bot.budget > 0]
        if len(active_bots) == 1:
            return active_bots[0]

        return None

    def play(self) -> None:
        """
        Main game loop that continues until the maximum number of rounds is reached or a winner is found.
        """
        while self.round <= self.max_steps and any(bot.budget > 0 for bot in self.bots):
            self.play_round()
            winner = self.check_for_winner()
            if winner:
                print(f"{winner.name} wins the game with a budget of {winner.budget}!")
                break
        else:
            print("Game ended due to step limit or all bots losing their budget.")
