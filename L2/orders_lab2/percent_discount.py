from discount import Discount


class PercentDiscount(Discount):
    def __init__(self, percent=10):
        if percent <= 0 or percent > 100:
            raise ValueError("Процент скидки должен быть от 1 до 100")
        self.percent = percent
        self.name = "скидка " + str(percent) + "%"

    def apply(self, order):
        order.discount_percent = min(100, order.discount_percent + self.percent)
