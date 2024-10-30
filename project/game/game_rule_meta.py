class GameRuleMeta(type):
    NUMBER_OF_FIELDS = 50
    WINNING_BUDGET = 1000

    def __new__(cls, name, bases, dct):
        dct["NUMBER_OF_FIELDS"] = cls.NUMBER_OF_FIELDS
        dct["WINNING_BUDGET"] = cls.WINNING_BUDGET
        return super().__new__(cls, name, bases, dct)
