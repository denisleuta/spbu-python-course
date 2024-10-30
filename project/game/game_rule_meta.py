class GameRuleMeta(type):
    """
    Metaclass for defining game rules and constants.

    This metaclass establishes common game rules and constants that can be shared
    across different game classes. It sets the number of fields available in the game
    and the budget required to achieve a win.

    Attributes:
        NUMBER_OF_FIELDS (int): The total number of fields available in the game (default is 50).
        WINNING_BUDGET (int): The budget required to win the game (default is 1000).

    Methods:
        __new__(cls, name, bases, dct):
            Creates a new class and adds game rule constants to the class dictionary.
            The constants NUMBER_OF_FIELDS and WINNING_BUDGET are added to any class
            that uses this metaclass.
    """
    NUMBER_OF_FIELDS = 50
    WINNING_BUDGET = 1000

    def __new__(cls, name, bases, dct):
        dct["NUMBER_OF_FIELDS"] = cls.NUMBER_OF_FIELDS
        dct["WINNING_BUDGET"] = cls.WINNING_BUDGET
        return super().__new__(cls, name, bases, dct)
