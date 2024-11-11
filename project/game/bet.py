from typing import Union


class Bet:
    """
    Represents a betting action in the game.

    The Bet class encapsulates the details of a bet placed by a bot or player,
    including the amount wagered, the type of bet, and the specific choice made.

    Attributes:
        amount (int): The amount of money wagered on the bet.
        bet_type (str): The type of bet being placed (e.g., "color", "number").
        choice (Union[str, int]): The specific choice associated with the bet.
            This can be either a string (for color bets) or an integer (for number bets).

    Methods:
        __init__(amount: int, bet_type: str, choice: Union[str, int]) -> None:
            Initializes a new Bet instance with the specified amount, bet type, and choice.
    """

    def __init__(self, amount: int, bet_type: str, choice: Union[str, int]) -> None:
        self.amount = amount
        self.bet_type = bet_type
        self.choice = choice
