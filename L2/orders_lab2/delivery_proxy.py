from delivery import Delivery


class DeliveryProxy(Delivery):
    def __init__(self, real_delivery, regions=None, fallback=None):
        self.real_delivery = real_delivery
        self.regions = regions
        self.fallback = fallback
        self.current = real_delivery
        self.cache = {}

    def log(self, text):
        print("    [DeliveryProxy] " + text)

    def check_real(self, order):
        if len(order.items) == 0:
            self.log("заказ #" + str(order.id) + " пустой")
            return False
        if self.regions is not None and order.region not in self.regions:
            self.log(self.real_delivery.name + " не работает в регионе " + order.region)
            return False
        if not self.real_delivery.is_available(order):
            self.log(self.real_delivery.name + " не подходит по весу ("
                     + str(round(order.get_total_weight(), 2)) + " кг)")
            return False
        return True

    def choose(self, order):
        if self.check_real(order):
            self.current = self.real_delivery
            return self.real_delivery
        if self.fallback is not None and self.fallback.is_available(order):
            self.log("переключаемся на " + self.fallback.name)
            self.current = self.fallback
            return self.fallback
        return None

    def is_available(self, order):
        self.log("is_available для заказа #" + str(order.id))
        return self.choose(order) is not None

    def get_cost(self, order):
        delivery = self.choose(order)
        if delivery is None:
            raise ValueError("Доставка недоступна для заказа #" + str(order.id))
        key = (delivery.name, round(order.get_total_weight(), 3))
        if key in self.cache:
            self.log("get_cost: берем из кеша " + str(self.cache[key]))
        else:
            self.cache[key] = delivery.get_cost(order)
            self.log("get_cost: считаем у " + delivery.name + " = " + str(self.cache[key]))
        return self.cache[key]

    def get_estimated_time(self):
        return self.current.get_estimated_time()

    def __getattr__(self, name):
        return getattr(self.current, name)
