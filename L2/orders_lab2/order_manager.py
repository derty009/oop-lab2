from observer import IObserver
from order import Order
from order_status import OrderStatus


class OrderManager(IObserver):
    def __init__(self, max_active_orders=5):
        self.orders = []
        self.customers = set()
        self.max_active_orders = max_active_orders
        self.active_orders = {}
        self.payments = {}
        self.bonuses = {}

    def create_order(self, customer, items, region="Москва"):
        if self.get_active_count(customer) >= self.max_active_orders:
            raise ValueError("У клиента " + customer + " уже "
                             + str(self.max_active_orders) + " активных заказов")
        order = Order(customer, region)
        for item in items:
            order.add_item(item)
        order.subscribe(self)

        self.orders.append(order)
        self.customers.add(customer)
        self.active_orders[customer] = self.get_active_count(customer) + 1
        return order

    def find_order(self, order_id):
        for order in self.orders:
            if order.id == order_id:
                return order
        return None

    def update_status(self, order_id, new_status):
        order = self.find_order(order_id)
        if order is None:
            raise ValueError("Заказ #" + str(order_id) + " не найден")
        order.set_status(new_status)

    def on_order_event(self, event):
        print("    [OrderManager] " + str(event))
        order = self.find_order(event.order_id)
        customer = order.customer

        if event.new_status == OrderStatus.PAID:
            cashback = order.get_cashback()
            self.payments[order.id] = (event.timestamp, order.get_total_price(), cashback)
            self.bonuses[customer] = self.get_bonus(customer) + cashback

        if event.new_status in (OrderStatus.DELIVERED, OrderStatus.CANCELLED):
            self.active_orders[customer] = self.get_active_count(customer) - 1

        if event.new_status == OrderStatus.CANCELLED:
            if order.id in self.payments:
                cashback = self.payments.pop(order.id)[2]
                self.bonuses[customer] = self.get_bonus(customer) - cashback
            self.update_customers(customer)

        if self.get_active_count(customer) > self.max_active_orders:
            print("    [OrderManager] превышен лимит активных заказов у " + customer)

    def update_customers(self, customer):
        for order in self.orders:
            if order.customer == customer and order.status != OrderStatus.CANCELLED:
                return
        self.customers.discard(customer)

    def get_turnover(self, date_from=None, date_to=None):
        total = 0
        for timestamp, amount, cashback in self.payments.values():
            if date_from is not None and timestamp < date_from:
                continue
            if date_to is not None and timestamp > date_to:
                continue
            total += amount
        return round(total, 2)

    def get_customer_count(self):
        return len(self.customers)

    def get_active_count(self, customer):
        return self.active_orders.get(customer, 0)

    def get_bonus(self, customer):
        return round(self.bonuses.get(customer, 0), 2)
