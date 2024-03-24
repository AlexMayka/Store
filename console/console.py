# Модуль для вывода товаров на консоль
# Содержит функцию для вывода товаров на консоль
from loggingApp.loggingApp import logger


def output_product(orders: list, products: list) -> None:
    """
    Функция для вывода товаров на консоль.

    :param orders: Список заказов, для которых нужно вывести товары
    :param products: Список товаров, которые нужно вывести
    :return: None
    """
    try:
        logger.info("Начало вывода товаров на консоль")

        # Создаем два словаря для хранения товаров на основных и дополнительных стеллажах
        main_shelf = {}
        additional_shelf = {}

        # Разделяем товары на основные и дополнительные стеллажи
        for product in products:
            id_product, shelf, is_main = product[0], product[5], product[4]
            if is_main:
                if shelf not in main_shelf:
                    main_shelf[shelf] = []
                main_shelf[shelf].append(product)
            else:
                if id_product not in additional_shelf:
                    additional_shelf[id_product] = []
                additional_shelf[id_product].append(shelf)

        # Выводим товары для каждого стеллажа
        print("=+=+=+=")
        print(f"Страница сборки заказов {','.join(orders)}")
        for shelf_name, products in sorted(main_shelf.items()):
            print(f"===Стеллаж {shelf_name}")
            for product in products:
                id_product, quantity, id_order, name = product[0:4]
                print(f"{name} (id={id_product})")
                print(f"заказ {id_order}, {quantity} шт")
                if id_product in additional_shelf:
                    print(f"доп стеллаж: {','.join(additional_shelf[id_product])}")
                print()

        logger.info("Успешный вывод товаров на консоль")
    except Exception as ex:
        logger.error(f"Ошибка при выводе товаров на консоль: {ex}")
