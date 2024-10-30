from project.bots.bot import Bot
from project.game.bet import Bet
from typing import Optional


class OnlyGreenBot(Bot):
    def place_bet(self) -> Optional[Bet]:
        if self.budget >= 10:
            # Всегда ставит на зеленое
            return Bet(amount=10, bet_type="color", choice="Green")
        return None
