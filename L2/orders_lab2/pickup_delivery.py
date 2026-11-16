from delivery import Delivery


class PickupDelivery(Delivery):
    def __init__(self):
        self.name = "Самовывоз"
        self.base_cost = 0
        self.max_weight = None

    def get_cost(self, order):
        return 0

    def get_estimated_time(self):
        return "1-3 дня"

    def is_available(self, order):
        return True
