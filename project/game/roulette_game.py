import random
from typing import List, Optional, Tuple
from project.bots.bot import Bot
from project.game.bet import Bet
from project.game.game_rule_meta import GameRuleMeta


class RouletteGame(metaclass=GameRuleMeta):
    """
    Represents a game of Roulette involving multiple betting bots.

    The RouletteGame class manages the game mechanics, including spinning the wheel,
    evaluating bets, and determining winners based on the outcomes of each round. 
    It allows multiple bots to participate and tracks their budgets throughout the game.

    Attributes:
        NUMBER_OF_FIELDS (int): The total number of fields in the roulette game (inherited from GameRuleMeta).
        WINNING_BUDGET (int): The budget required to win the game (inherited from GameRuleMeta).
        COLORS (List[str]): A list of colors used in the roulette game (Red, Black, Green).
        WINNING_MULTIPLIER_COLOR (int): The multiplier for winning color bets.
        WINNING_MULTIPLIER_NUMBER (int): The multiplier for winning number bets.
        WINNING_MULTIPLIER_GREEN (int): The multiplier for winning bets on Green.

    Methods:
        __init__(bots: List[Bot], max_steps: int = 10) -> None:
            Initializes a new instance of RouletteGame with a list of bots and a maximum number of rounds.

        spin_wheel() -> Tuple[int, str]:
            Simulates spinning the roulette wheel and returns the result number and corresponding color.

        evaluate_bets(bet: Bet, result_number: int, result_color: str) -> int:
            Evaluates a bet based on the outcome of the spin and returns the resulting amount won or lost.

        display_state() -> None:
            Displays the current state of the game, including each bot's budget at the start of a round.

        play_round() -> None:
            Conducts a single round of betting, spinning the wheel, evaluating bets, updating bot budgets,
            and displaying results.

        check_for_winner() -> Optional[Bot]:
            Checks if any bot has reached the winning budget or if only one bot remains active. 
            Returns the winning bot if found, otherwise returns None.

        play() -> None:
            Manages the overall game loop, playing rounds until either the maximum steps are reached
            or all bots have lost their budgets. Declares a winner if applicable.
    """
    NUMBER_OF_FIELDS: int
    WINNING_BUDGET: int

    COLORS = ["Red", "Black", "Green"]
    WINNING_MULTIPLIER_COLOR = 2
    WINNING_MULTIPLIER_NUMBER = 36
    WINNING_MULTIPLIER_GREEN = 35

    def __init__(self, bots: List[Bot], max_steps: int = 10) -> None:
        self.bots = bots
        self.round = 1
        self.max_steps = max_steps

    def spin_wheel(self) -> Tuple[int, str]:
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
        if bet.bet_type == "color" and bet.choice == result_color:
            return bet.amount * (
                self.WINNING_MULTIPLIER_GREEN
                if result_color == "Green"
                else self.WINNING_MULTIPLIER_COLOR
            )
        elif bet.bet_type == "number" and bet.choice == result_number:
            return bet.amount * self.WINNING_MULTIPLIER_NUMBER
        return -bet.amount

    def display_state(self) -> None:
        print(f"Round {self.round}:")
        for bot in self.bots:
            print(f"  {bot.name} budget: {bot.budget}")
        print("-" * 30)

    def play_round(self) -> None:
        result_number, result_color = self.spin_wheel()
        print(f"Roulette spun to {result_number} ({result_color})")
        for bot in self.bots:
            if bot.budget > 0:
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
        while self.round <= self.max_steps and any(bot.budget > 0 for bot in self.bots):
            self.play_round()
            winner = self.check_for_winner()
            if winner:
                print(f"{winner.name} wins the game with a budget of {winner.budget}!")
                break
        else:
            print("Game ended due to step limit or all bots losing their budget.")
