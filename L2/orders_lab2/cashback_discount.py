from discount import Discount


class CashbackDiscount(Discount):
    def __init__(self, percent=5):
        if percent <= 0 or percent > 100:
            raise ValueError("Процент кэшбэка должен быть от 1 до 100")
        self.percent = percent
        self.name = "кэшбэк " + str(percent) + "%"

    def apply(self, order):
        order.cashback_percent = min(100, order.cashback_percent + self.percent)
