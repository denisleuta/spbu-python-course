from typing import Optional, Dict
from project.game.bet import Bet


class StrategyMeta(type):
    """
    Metaclass for registering different bot strategies dynamically.
    """

    strategies: Dict[str, type] = {}

    def __new__(cls, name, bases, dct):
        new_cls = super().__new__(cls, name, bases, dct)
        if name != "Bot":
            cls.strategies[name] = new_cls
        return new_cls

    @classmethod
    def create_strategy(cls, strategy_name: str, **kwargs):
        """Create a new instance of the strategy with given kwargs."""
        if strategy_name not in cls.strategies:
            raise ValueError(f"Strategy '{strategy_name}' not found.")
        return cls.strategies[strategy_name](**kwargs)

    @classmethod
    def get_strategies(cls):
        """Return the registered strategies."""
        return cls.strategies


class Bot(metaclass=StrategyMeta):
    def __init__(self, name: str, budget: int) -> None:
        self.name = name
        self.budget = budget

    def place_bet(self) -> Optional[Bet]:
        pass

    def update_budget(self, amount: int) -> None:
        self.budget += amount
