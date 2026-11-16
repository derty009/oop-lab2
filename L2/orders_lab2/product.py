class Product:
    next_id = 1

    def __init__(self, product_type, quantity=1, current_price=None):
        if quantity <= 0:
            raise ValueError("Количество должно быть больше нуля")
        if current_price is None:
            current_price = product_type.base_price
        if current_price < 0:
            raise ValueError("Цена не может быть отрицательной")

        self.id = Product.next_id
        Product.next_id += 1
        self.type = product_type
        self.quantity = quantity
        self.current_price = current_price

    def get_weight(self):
        return self.type.base_weight * self.quantity

    def get_total_price(self):
        return self.current_price * self.quantity

    def change_quantity(self, delta):
        if self.quantity + delta <= 0:
            raise ValueError("Количество должно быть больше нуля")
        self.quantity += delta

    def copy(self):
        return Product(self.type, self.quantity, self.current_price)

    def __str__(self):
        return (self.type.category + " x" + str(self.quantity)
                + " по " + str(self.current_price) + " = " + str(self.get_total_price()))
