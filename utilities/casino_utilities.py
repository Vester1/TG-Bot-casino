from aiogram.types import Message
from keyboards.casino_keyboards import get_keyboard_bet


anims = ['CgACAgQAAxkBAAIBGmWQMZuI4A3ZRC4dl7N76a5Z8AYYAAIkAwACBhcEU_zzWc930Hi_NAQ',
         'CgACAgQAAxkBAAIBG2WQMZsG_Be6X1VdBpXtawiz6yluAAI-AwACd1kFUzZ_JAi7KSw3NAQ',
         'CgACAgQAAxkBAAIBHGWQMZ4EicY5eZvwWHL-7FfkYvhpAAJDAwACgLoFUwJdqgTO1ShQNAQ',
         'CgACAgIAAxkBAAIBHmWQMaAKxpad-byyLf8JT01R7QyrAAKpGAACUFQBScrfAAEC2M66KDQE']
stickers = [
            'CAACAgIAAxkBAAICW2WRXat3Shp3fvBzXhOSyqeTEXJ3AAILAAMlUKUZJ0I9amwv-1A0BA',
            'CAACAgIAAxkBAAICXWWRXawrtzCMCXqiU424Cs0AAbUkqAACBgADJVClGXvbdXDWg3gQNAQ',
            'CAACAgIAAxkBAAICX2WRXa574pyEut2FqIIWcGD2J-mIAAIVAAMlUKUZf-Mqb9sL4_s0BA',
            'CAACAgIAAxkBAAICYWWRXbFx2rjntcRyOy-K839e1CA6AAJRAAMlUKUZmeS50x0o3fs0BA',
            'CAACAgIAAxkBAAICY2WRXbND7vV-7lNKdRU02vfULmFjAAJoAAMlUKUZKElkah7EMdQ0BA',
            'CAACAgIAAxkBAAICZWWRXbX-lngnQ8CWCreZcha19Jf5AAJ5AAMlUKUZInGTvhbMRgU0BA',
            'CAACAgIAAxkBAAICZ2WRXbYzPYwwSZt6Wn5kuB2TCyTIAAJ1AAMlUKUZcm9by53wzDw0BA',
            'CAACAgIAAxkBAAICaWWRXbjwz-jn0QRvCwyMKHPv7D7JAAKLAAMlUKUZxPevk94tTNU0BA',
            'CAACAgIAAxkBAAICa2WRXbm5BOKSVmcOsURojzdOVpf1AAKgAAMlUKUZcetTAdja41g0BA',
            'CAACAgIAAxkBAAICbWWRXboyXhMO49zCJVIzaYmMs5yTAAKWAAMlUKUZHwTRPdbgNLA0BA',
    ]


async def update_bet_text(message: Message, new_value: int):
    await message.edit_text(
        f"Ставка: {new_value}",
        reply_markup=get_keyboard_bet()
    )