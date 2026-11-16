class ProductType:
    catalog = {
        "Смартфон": (0.3, 30000),
        "Ноутбук": (2.5, 80000),
        "Книга": (0.5, 700),
        "Телевизор": (12.0, 45000),
        "Холодильник": (60.0, 50000),
        "Кружка": (0.4, 500),
    }
    pool = {}

    def __init__(self, category, base_weight, base_price):
        self.category = category
        self.base_weight = base_weight
        self.base_price = base_price

    @staticmethod
    def get_type(category):
        if category not in ProductType.pool:
            if category not in ProductType.catalog:
                raise ValueError("Нет такого типа товара: " + category)
            weight, price = ProductType.catalog[category]
            ProductType.pool[category] = ProductType(category, weight, price)
        return ProductType.pool[category]
