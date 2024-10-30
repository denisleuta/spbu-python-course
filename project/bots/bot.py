from typing import Optional, Dict
from project.game.bet import Bet


class StrategyMeta(type):
    """
    Metaclass for dynamically registering different bot strategies.

    This metaclass allows for the registration of bot strategies by storing
    them in a dictionary. It enables the creation of new strategy instances
    and retrieval of all registered strategies.

    Attributes:
        strategies (Dict[str, type]): A dictionary mapping strategy names to their corresponding classes.

    Methods:
        __new__(cls, name, bases, dct):
            Creates a new class and registers it if it is not the base Bot class.

        create_strategy(cls, strategy_name: str, **kwargs):
            Creates a new instance of the specified strategy using the provided keyword arguments.
            Raises ValueError if the strategy is not found.

        get_strategies(cls):
            Returns a dictionary of all registered strategies.
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
    """
    Base class for all betting bots.

    This class serves as a blueprint for creating different types of betting bots,
    providing common attributes and methods that can be extended by specific strategies.

    Attributes:
        name (str): The name of the bot.
        budget (int): The current budget available for placing bets.

    Methods:
        place_bet() -> Optional[Bet]:
            Abstract method to be implemented by subclasses for placing bets.

        update_budget(amount: int) -> None:
            Updates the bot's budget by adding the specified amount.
    """

    def __init__(self, name: str, budget: int) -> None:
        self.name = name
        self.budget = budget

    def place_bet(self) -> Optional[Bet]:
        pass

    def update_budget(self, amount: int) -> None:
        self.budget += amount
