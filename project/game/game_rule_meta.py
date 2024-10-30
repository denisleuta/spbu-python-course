class GameRuleMeta(type):
    def __new__(cls, name, bases, dct):
        dct["NUMBER_OF_FIELDS"] = 50
        dct["WINNING_BUDGET"] = 1000
        return super().__new__(cls, name, bases, dct)
