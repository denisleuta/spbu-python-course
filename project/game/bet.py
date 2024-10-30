from typing import Union


class Bet:
    def __init__(self, amount: int, bet_type: str, choice: Union[int, str]) -> None:
        self.amount = amount
        self.bet_type = bet_type
        self.choice = choice
