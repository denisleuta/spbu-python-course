from typing import Optional
from project.game.bet import Bet


class StrategyMeta(type):
    strategies: dict[str, type] = {}

    def __new__(cls, name, bases, dct):
        new_cls = super().__new__(cls, name, bases, dct)
        if name != "Bot":
            StrategyMeta.strategies[name] = new_cls
        return new_cls


class Bot(metaclass=StrategyMeta):
    def __init__(self, name: str, budget: int) -> None:
        self.name = name
        self.budget = budget

    def place_bet(self) -> Optional[Bet]:
        pass

    def update_budget(self, amount: int) -> None:
        self.budget += amount
