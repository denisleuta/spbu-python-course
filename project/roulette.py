import random
from typing import List, Optional, Tuple


class Bet:
    def __init__(self, amount: int, bet_type: str, choice: int | str) -> None:
        self.amount = amount
        self.bet_type = bet_type
        self.choice = choice


class Bot:
    def __init__(self, name: str, budget: int) -> None:
        self.name = name
        self.budget = budget

    def place_bet(self) -> Optional[Bet]:
        pass

    def update_budget(self, amount: int) -> None:
        self.budget += amount


class ConservativeBot(Bot):
    def place_bet(self) -> Optional[Bet]:
        if self.budget > 0:
            return Bet(amount=10, bet_type="color", choice="Red")
        return None


class AggressiveBot(Bot):
    def place_bet(self) -> Optional[Bet]:
        if self.budget > 0:
            number_choice = random.randint(1, 36)
            return Bet(amount=50, bet_type="number", choice=number_choice)
        return None


class RandomBot(Bot):
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
    COLORS = ["Red", "Black", "Green"]
    MAX_STEPS = 10

    def __init__(self, bots: List[Bot]) -> None:
        self.bots = bots
        self.round = 1

    def spin_wheel(self) -> Tuple[int, str]:
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
        if bet.bet_type == "color" and bet.choice == result_color:
            return bet.amount * (35 if result_color == "Green" else 2)
        elif bet.bet_type == "number" and bet.choice == result_number:
            return bet.amount * 36
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
            bet = bot.place_bet()
            if bet:
                outcome = self.evaluate_bets(bet, result_number, result_color)
                bot.update_budget(outcome)
                print(
                    f"{bot.name} bet {bet.amount} on {bet.choice} ({bet.bet_type}) and {'won' if outcome > 0 else 'lost'} {abs(outcome)}"
                )

        self.display_state()
        self.round += 1

    def play(self) -> None:
        while self.round <= self.MAX_STEPS and any(bot.budget > 0 for bot in self.bots):
            self.play_round()
