from discount import Discount
from product import Product
from product_type import ProductType


class GiftDiscount(Discount):
    def __init__(self, category="Кружка"):
        self.category = category
        self.name = "подарок: " + category

    def apply(self, order):
        order.items.append(Product(ProductType.get_type(self.category), 1, 0))
