from delivery import Delivery


class PostDelivery(Delivery):
    def __init__(self):
        self.name = "Почта"
        self.base_cost = 200
        self.max_weight = 10

    def get_cost(self, order):
        weight = order.get_total_weight()
        if weight <= 2:
            return self.base_cost
        return round(self.base_cost + (weight - 2) * 30, 2)

    def get_estimated_time(self):
        return "5-10 дней"

    def is_available(self, order):
        return order.get_total_weight() <= self.max_weight
