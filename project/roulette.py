import random
from typing import List, Optional, Tuple


class Bet:
    """
    Represents a bet placed by a bot in the game of Roulette.

    Attributes:
        amount (int): The amount of money bet.
        bet_type (str): The type of bet (e.g., 'color' or 'number').
        choice (int | str): The choice made for the bet, either a color or a specific number.
    """

    def __init__(self, amount: int, bet_type: str, choice: int | str) -> None:
        self.amount = amount
        self.bet_type = bet_type
        self.choice = choice


class Bot:
    """
    Represents a bot in the game with a specific betting strategy.

    Attributes:
        name (str): The name of the bot.
        budget (int): The current budget of the bot.

    Methods:
        place_bet() -> Optional[Bet]: Places a bet based on the bot's strategy (to be implemented in subclasses).
        update_budget(amount: int) -> None: Updates the bot's budget based on the outcome of a bet.
    """

    def __init__(self, name: str, budget: int) -> None:
        self.name = name
        self.budget = budget

    def place_bet(self) -> Optional[Bet]:
        """
        Placeholder method for placing a bet. To be implemented in subclasses.

        Returns:
            Optional[Bet]: The bet placed by the bot, or None if no bet is placed.
        """
        pass

    def update_budget(self, amount: int) -> None:
        """
        Updates the bot's budget by the specified amount.

        Args:
            amount (int): The amount to add to the budget (can be negative if the bot loses the bet).
        """
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


class RouletteGame:
    """
    Represents a game of Roulette, with multiple bots and a spinning wheel.

    Attributes:
        COLORS (List[str]): Available colors in the roulette game.
        MAX_STEPS (int): Maximum number of rounds to play.
        bots (List[Bot]): List of bots participating in the game.
        round (int): Current round of the game.

    Methods:
        spin_wheel() -> Tuple[int, str]: Simulates a spin of the roulette wheel, returning a number and a color.
        evaluate_bets(bet: Bet, result_number: int, result_color: str) -> int: Determines the outcome of a bet.
        display_state() -> None: Displays the current state of the game.
        play_round() -> None: Conducts a single round of the game.
        check_for_winner() -> Optional[Bot]: Checks if there is a single winner with budget left.
        play() -> None: Plays the game until a winner is determined or the maximum rounds are reached.
    """

    COLORS = ["Red", "Black", "Green"]
    MAX_STEPS = 10

    def __init__(self, bots: List[Bot]) -> None:
        self.bots = bots
        self.round = 1

    def spin_wheel(self) -> Tuple[int, str]:
        """
        Spins the roulette wheel, producing a random number and associated color.

        Returns:
            Tuple[int, str]: The number and color resulting from the spin.
        """
        result_number = random.randint(0, 36)
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
        Evaluates a bet based on the roulette spin result.

        Args:
            bet (Bet): The bet placed by the bot.
            result_number (int): The number that was spun.
            result_color (str): The color that was spun.

        Returns:
            int: The amount won or lost from the bet.
        """
        if bet.bet_type == "color" and bet.choice == result_color:
            return bet.amount * (35 if result_color == "Green" else 2)
        elif bet.bet_type == "number" and bet.choice == result_number:
            return bet.amount * 36
        return -bet.amount

    def display_state(self) -> None:
        """
        Displays the current state of the game, including round and each bot's budget.
        """
        print(f"Round {self.round}:")
        for bot in self.bots:
            print(f"  {bot.name} budget: {bot.budget}")
        print("-" * 30)

    def play_round(self) -> None:
        """
        Conducts a single round of the game, allowing each bot to place a bet and updating budgets.
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
        """
        Checks if there is a single winner, i.e., only one bot has a positive budget.

        Returns:
            Optional[Bot]: The winning bot if found, otherwise None.
        """
        active_bots = [bot for bot in self.bots if bot.budget > 0]
        if len(active_bots) == 1:
            return active_bots[0]
        return None

    def play(self) -> None:
        """
        Plays the game of Roulette until a winner is determined or the maximum rounds are reached.
        """
        while self.round <= self.MAX_STEPS and any(bot.budget > 0 for bot in self.bots):
            self.play_round()
            winner = self.check_for_winner()
            if winner:
                print(f"{winner.name} wins the game with a budget of {winner.budget}!")
                break
        else:
            print("Game ended due to step limit or all bots losing their budget.")
