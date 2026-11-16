class IObservable:
    def __init__(self):
        self.observers = []

    def subscribe(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def unsubscribe(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def notify(self, event):
        for observer in list(self.observers):
            observer.on_order_event(event)
