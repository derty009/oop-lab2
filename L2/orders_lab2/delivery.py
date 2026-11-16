from abc import ABC, abstractmethod


class Delivery(ABC):
    @abstractmethod
    def get_cost(self, order):
        pass

    @abstractmethod
    def get_estimated_time(self):
        pass

    @abstractmethod
    def is_available(self, order):
        pass

    def __lshift__(self, order):
        order.set_delivery(self)
        return order
