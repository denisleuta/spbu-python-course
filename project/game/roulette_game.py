import random
from typing import List, Optional, Tuple
from project.bots.bot import Bot
from project.game.bet import Bet
from project.game.game_rule_meta import GameRuleMeta


class RouletteGame(metaclass=GameRuleMeta):
    COLORS = ["Red", "Black", "Green"]

    def __init__(self, bots: List[Bot], max_steps: int = 10) -> None:
        self.bots = bots
        self.round = 1
        self.max_steps = max_steps

    def spin_wheel(self) -> Tuple[int, str]:
        result_number = random.randint(0, self.NUMBER_OF_FIELDS - 1)
        result_color = "Green" if result_number == 0 else "Red" if result_number % 2 == 0 else "Black"
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
                print(f"{bot.name} bet {bet.amount} on {bet.choice} ({bet.bet_type}) and {'won' if outcome > 0 else 'lost'} {abs(outcome)}")
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
