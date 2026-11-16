from datetime import datetime, timedelta

from cashback_discount import CashbackDiscount
from courier_delivery import CourierDelivery
from delivery_proxy import DeliveryProxy
from free_delivery_discount import FreeDeliveryDiscount
from gift_discount import GiftDiscount
from order_manager import OrderManager
from order_status import OrderStatus
from percent_discount import PercentDiscount
from pickup_delivery import PickupDelivery
from post_delivery import PostDelivery
from product import Product
from product_type import ProductType


def make_product(category, quantity=1):
    return Product(ProductType.get_type(category), quantity)


def demo_create_order():
    print()
    print("--- Сценарий 1: создание заказа и процентная скидка ---")
    manager = OrderManager()
    order = manager.create_order("Иван", [make_product("Смартфон"), make_product("Книга", 2)])
    order.add_item(make_product("Ноутбук"))
    print(order)

    order = order + PercentDiscount(10)
    print("После order + PercentDiscount(10):")
    print(order)

    print("Один и тот же тип товара в пуле:",
          ProductType.get_type("Книга") is order.get_items()[1].type)


def demo_delivery():
    print()
    print("--- Сценарий 2: выбор доставки через delivery << order ---")
    manager = OrderManager()
    courier = DeliveryProxy(CourierDelivery(), regions=["Москва", "Санкт-Петербург"],
                            fallback=PostDelivery())

    order = manager.create_order("Иван", [make_product("Смартфон"), make_product("Книга")])
    courier << order
    print(order)
    print("Повторный расчет стоимости:", order.get_delivery_cost())
    print("Имя через __getattr__ прокси:", courier.name, ", лимит веса:", courier.max_weight)

    print()
    print("Заказ в Казань, курьер там не работает:")
    kazan_order = manager.create_order("Петр", [make_product("Книга", 3)], region="Казань")
    courier << kazan_order
    print(kazan_order)

    print()
    print("Холодильник 60 кг:")
    fridge_order = manager.create_order("Анна", [make_product("Холодильник")])
    try:
        courier << fridge_order
    except ValueError as error:
        print("Ошибка:", error)
    PickupDelivery() << fridge_order
    print(fridge_order)


def demo_observer():
    print()
    print("--- Сценарий 3: смена статуса и уведомление OrderManager ---")
    manager = OrderManager()
    order = manager.create_order("Иван", [make_product("Телевизор")])
    order + CashbackDiscount(5)
    DeliveryProxy(CourierDelivery()) << order

    print("Оборот до оплаты:", manager.get_turnover())
    manager.update_status(order.id, OrderStatus.PAID)
    print("Оборот после оплаты:", manager.get_turnover())
    print("Бонусы Ивана:", manager.get_bonus("Иван"))

    manager.update_status(order.id, OrderStatus.SHIPPED)
    manager.update_status(order.id, OrderStatus.DELIVERED)
    print("Активных заказов у Ивана:", manager.get_active_count("Иван"))

    yesterday = datetime.now() - timedelta(days=1)
    print("Оборот за последние сутки:", manager.get_turnover(yesterday, datetime.now()))
    print("Оборот до вчерашнего дня:", manager.get_turnover(None, yesterday))

    print("Пробуем вернуть доставленный заказ в pending:")
    try:
        manager.update_status(order.id, OrderStatus.PENDING)
    except ValueError as error:
        print("Ошибка:", error)


def demo_many_discounts():
    print()
    print("--- Сценарий 4: несколько скидок в одном заказе ---")
    manager = OrderManager()
    order = manager.create_order("Мария", [make_product("Ноутбук"), make_product("Книга", 4)])
    PostDelivery() << order
    print(order)

    without_discounts = order.copy()

    order = order + PercentDiscount(10)
    print("После скидки 10%:", order.get_total_price())
    order = order + CashbackDiscount(5)
    print("После кэшбэка 5%:", order.get_total_price(), ", кэшбэк:", order.get_cashback())
    order = order + FreeDeliveryDiscount()
    print("После бесплатной доставки:", order.get_total_price())
    order = order + GiftDiscount("Кружка")
    print("После подарка:", order.get_total_price())
    print(order)

    print()
    print("Копия заказа без скидок:")
    print(without_discounts)
    print("Заказ со скидками дешевле копии:", order < without_discounts)


def demo_cancel():
    print()
    print("--- Сценарий 5: отмена заказа и лимит активных заказов ---")
    manager = OrderManager(max_active_orders=5)

    orders = []
    for i in range(5):
        orders.append(manager.create_order("Олег", [make_product("Книга")]))
    print("Создано заказов у Олега:", manager.get_active_count("Олег"))

    try:
        manager.create_order("Олег", [make_product("Книга")])
    except ValueError as error:
        print("Ошибка:", error)

    manager.update_status(orders[0].id, OrderStatus.CANCELLED)
    print("После отмены активных заказов:", manager.get_active_count("Олег"))
    manager.create_order("Олег", [make_product("Книга")])
    print("Новый заказ создан, активных:", manager.get_active_count("Олег"))

    print()
    lena_order = manager.create_order("Лена", [make_product("Смартфон")])
    manager.update_status(lena_order.id, OrderStatus.PAID)
    print("Клиентов:", manager.get_customer_count(), ", оборот:", manager.get_turnover())
    manager.update_status(lena_order.id, OrderStatus.CANCELLED)
    print("После отмены заказа Лены клиентов:", manager.get_customer_count(),
          ", оборот:", manager.get_turnover())


def main():
    while True:
        print()
        print("===== МЕНЮ =====")
        print("1 - создание заказа и скидка")
        print("2 - выбор доставки и прокси")
        print("3 - смена статуса и наблюдатель")
        print("4 - несколько скидок в одном заказе")
        print("5 - отмена заказа и лимиты")
        print("0 - выход")

        try:
            choice = input("Выбор: ")
        except EOFError:
            break

        if choice == "1":
            demo_create_order()
        elif choice == "2":
            demo_delivery()
        elif choice == "3":
            demo_observer()
        elif choice == "4":
            demo_many_discounts()
        elif choice == "5":
            demo_cancel()
        elif choice == "0":
            break
        else:
            print("Нет такого пункта")


if __name__ == "__main__":
    main()
