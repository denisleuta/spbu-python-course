from project.bots.bot import Bot
from project.game.bet import Bet
from typing import Optional


class ConservativeBot(Bot):
    def place_bet(self) -> Optional[Bet]:
        if self.budget > 0:
            return Bet(amount=10, bet_type="color", choice="Red")
        return None
