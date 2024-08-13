from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery

from utilities.utilities import BETS


class IsValidBet(BaseFilter):
    def __init__(self):
        self.bets = BETS

    async def __call__(self, callback: CallbackQuery, balance: list[int]):
        bet = self.bets.get(callback.from_user.id, 0)
        return callback.data in ['🎰', '🎲', '🎯', '🎳', '🏀', '⚽'] and (bet == 0 or bet > balance[0])

