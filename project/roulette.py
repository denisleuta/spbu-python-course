import random

class Wheel:
    """Class to represent the roulette wheel."""
    def __init__(self):
        self.colors = ['Red', 'Black', 'Green']  # Green for the zero
        self.numbers = list(range(0, 37))  # European roulette: numbers 0 to 36

    def spin(self):
        number = random.choice(self.numbers)
        color = 'Green' if number == 0 else ('Red' if number % 2 == 0 else 'Black')
        return number, color


class Bet:
    """Class to represent a bet."""
    def __init__(self, amount, bet_type, choice):
        self.amount = amount
        self.bet_type = bet_type
        self.choice = choice

    def evaluate(self, outcome):
        """Evaluate bet based on outcome."""
        number, color = outcome
        if self.bet_type == 'color' and color == self.choice:
            return 2 * self.amount  # Double the amount for color bet
        elif self.bet_type == 'number':
            if number == self.choice:
                return 36 * self.amount if self.choice != 0 else 37 * self.amount  # Higher payout for zero
        return 0  # No winnings if the bet didn't match


class Bot:
    """Base bot class."""
    def __init__(self, name, budget):
        self.name = name
        self.budget = budget

    def place_bet(self):
        """Method to be implemented by subclasses with different strategies."""
        raise NotImplementedError


class ConservativeBot(Bot):
    """Bot that bets conservatively on color 'Red'."""
    def place_bet(self):
        if self.budget > 0:
            return Bet(amount=10, bet_type='color', choice='Red')
        return None


class AggressiveBot(Bot):
    """Bot that bets aggressively on specific numbers."""
    def place_bet(self):
        if self.budget > 0:
            number_choice = random.randint(1, 36)
            return Bet(amount=50, bet_type='number', choice=number_choice)
        return None


class RandomBot(Bot):
    """Bot that places random bets."""
    def place_bet(self):
        if self.budget > 0:
            bet_type = random.choice(['color', 'number'])
            if bet_type == 'color':
                color_choice = random.choice(['Red', 'Black'])
                return Bet(amount=20, bet_type='color', choice=color_choice)
            else:
                number_choice = random.randint(0, 36)  # Now includes 0
                return Bet(amount=20, bet_type='number', choice=number_choice)
        return None


class Game:
    """Class to control the game flow."""
    def __init__(self, bots, max_rounds=10):
        self.bots = bots
        self.wheel = Wheel()
        self.round = 0
        self.max_rounds = max_rounds

    def play_round(self):
        """Play a single round and evaluate bets."""
        print(f"\n--- Round {self.round + 1} ---")
        outcome = self.wheel.spin()
        print(f"Wheel spun: Number {outcome[0]}, Color {outcome[1]}")
        
        for bot in self.bots:
            bet = bot.place_bet()
            if bet:
                print(f"{bot.name} bets {bet.amount} on {bet.bet_type} '{bet.choice}'")
                winnings = bet.evaluate(outcome)
                bot.budget += winnings - bet.amount
                print(f"{bot.name} {'wins' if winnings else 'loses'}! New budget: {bot.budget}")

    def show_status(self):
        """Show the current status of the game."""
        print("\n--- Game Status ---")
        for bot in self.bots:
            print(f"{bot.name}: Budget = {bot.budget}")
        print(f"Rounds played: {self.round}\n")

    def play(self):
        """Play the game until win condition or maximum rounds."""
        while self.round < self.max_rounds:
            if any(bot.budget >= 1000 for bot in self.bots):  # Win condition
                print("Game over! We have a winner.")
                break
            self.play_round()
            self.round += 1
            self.show_status()


# Initialize bots and start the game
bots = [ConservativeBot('Bot1', 100), AggressiveBot('Bot2', 100), RandomBot('Bot3', 100)]
game = Game(bots)
game.play()
