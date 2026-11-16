from delivery import Delivery


class CourierDelivery(Delivery):
    def __init__(self):
        self.name = "Курьер"
        self.base_cost = 500
        self.max_weight = 20

    def get_cost(self, order):
        weight = order.get_total_weight()
        if weight <= 5:
            return self.base_cost
        return round(self.base_cost + (weight - 5) * 50, 2)

    def get_estimated_time(self):
        return "1-2 дня"

    def is_available(self, order):
        return order.get_total_weight() <= self.max_weight
