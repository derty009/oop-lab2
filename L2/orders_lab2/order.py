from observable import IObservable
from order_event import OrderEvent
from order_status import OrderStatus


class Order(IObservable):
    next_id = 1

    transitions = {
        OrderStatus.PENDING: [OrderStatus.PAID, OrderStatus.CANCELLED],
        OrderStatus.PAID: [OrderStatus.SHIPPED, OrderStatus.CANCELLED],
        OrderStatus.SHIPPED: [OrderStatus.DELIVERED],
        OrderStatus.DELIVERED: [],
        OrderStatus.CANCELLED: [],
    }

    def __init__(self, customer, region="Москва"):
        super().__init__()
        self.id = Order.next_id
        Order.next_id += 1
        self.customer = customer
        self.region = region
        self.items = []
        self.status = OrderStatus.PENDING
        self.delivery = None
        self.discounts = []
        self.discount_percent = 0
        self.cashback_percent = 0
        self.free_delivery = False

    def check_pending(self):
        if self.status != OrderStatus.PENDING:
            raise ValueError("Заказ #" + str(self.id) + " уже нельзя изменить")

    def add_item(self, product):
        self.check_pending()
        self.items.append(product)

    def remove_item(self, product_id):
        self.check_pending()
        for i in range(len(self.items)):
            if self.items[i].id == product_id:
                return self.items.pop(i)
        raise ValueError("Товар с id " + str(product_id) + " не найден в заказе")

    def get_items(self):
        return tuple(self.items)

    def get_total_weight(self):
        weight = 0
        for item in self.items:
            weight += item.get_weight()
        return weight

    def get_items_price(self):
        price = 0
        for item in self.items:
            price += item.get_total_price()
        return price * (100 - self.discount_percent) / 100

    def get_delivery_cost(self):
        if self.delivery is None or self.free_delivery:
            return 0
        return self.delivery.get_cost(self)

    def get_total_price(self):
        return round(self.get_items_price() + self.get_delivery_cost(), 2)

    def get_cashback(self):
        return round(self.get_items_price() * self.cashback_percent / 100, 2)

    def set_delivery(self, delivery):
        self.check_pending()
        if not delivery.is_available(self):
            raise ValueError("Доставка недоступна для заказа #" + str(self.id))
        self.delivery = delivery

    def apply_discount(self, discount):
        self.check_pending()
        discount.apply(self)
        self.discounts.append(discount)

    def set_status(self, new_status):
        if new_status not in Order.transitions[self.status]:
            raise ValueError("Нельзя перевести заказ из " + self.status.value
                             + " в " + new_status.value)
        if new_status == OrderStatus.PAID and len(self.items) == 0:
            raise ValueError("Нельзя оплатить пустой заказ")
        if new_status == OrderStatus.SHIPPED:
            if self.delivery is None or not self.delivery.is_available(self):
                raise ValueError("У заказа нет доступной доставки")

        old_status = self.status
        self.status = new_status
        self.notify(OrderEvent(self.id, old_status, new_status))

    def copy(self):
        new_order = Order(self.customer, self.region)
        for item in self.items:
            new_order.items.append(item.copy())
        new_order.delivery = self.delivery
        new_order.discounts = list(self.discounts)
        new_order.discount_percent = self.discount_percent
        new_order.cashback_percent = self.cashback_percent
        new_order.free_delivery = self.free_delivery
        return new_order

    def __add__(self, discount):
        self.apply_discount(discount)
        return self

    def __lt__(self, other):
        return self.get_total_price() < other.get_total_price()

    def __str__(self):
        text = ("Заказ #" + str(self.id) + " (" + self.customer + ", " + self.region + ")"
                + " статус: " + self.status.value + "\n")
        for item in self.items:
            text += "    " + str(item) + "\n"
        if self.delivery is None:
            text += "    доставка: не выбрана\n"
        else:
            text += ("    доставка: " + self.delivery.name + ", "
                     + self.delivery.get_estimated_time()
                     + ", стоимость " + str(self.get_delivery_cost()) + "\n")
        if len(self.discounts) > 0:
            names = []
            for discount in self.discounts:
                names.append(discount.name)
            text += "    акции: " + ", ".join(names) + "\n"
        text += ("    вес: " + str(round(self.get_total_weight(), 2)) + " кг"
                 + ", итого: " + str(self.get_total_price())
                 + ", кэшбэк: " + str(self.get_cashback()))
        return text
