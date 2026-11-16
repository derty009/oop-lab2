from discount import Discount


class FreeDeliveryDiscount(Discount):
    def __init__(self):
        self.name = "бесплатная доставка"

    def apply(self, order):
        order.free_delivery = True
