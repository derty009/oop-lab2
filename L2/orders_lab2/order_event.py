from datetime import datetime


class OrderEvent:
    def __init__(self, order_id, old_status, new_status):
        self.order_id = order_id
        self.old_status = old_status
        self.new_status = new_status
        self.timestamp = datetime.now()

    def __str__(self):
        return ("Заказ #" + str(self.order_id) + ": " + self.old_status.value
                + " -> " + self.new_status.value
                + " (" + self.timestamp.strftime("%H:%M:%S") + ")")
