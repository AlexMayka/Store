# Модуль для вывода товаров на консоль
# Содержит функцию для вывода товаров на консоль

from loggingApp.loggingApp import logger


def outputProduct(orders: list, products: list) -> None:
    """
    Функция для вывода товаров на консоль
    :param orders: Список заказов
    :param products: Список товаров
    :return: None
    """

    try:
        logger.info("Statr output console")
        mainShelf = {}
        additionalShelf = {}
        for product in products:
            idProduct, shelf, isMain = product[0], product[4], product[5]
            if isMain is True:
                if shelf not in mainShelf:
                    mainShelf[shelf] = []
                mainShelf[shelf].append(product)
            else:
                if idProduct not in additionalShelf:
                    additionalShelf[idProduct] = []
                additionalShelf[idProduct].append(shelf)

        # вывести товары для каждого стеллажа
        print("=+=+=+=")
        print(f"Страница сборки заказов {','.join(orders)}")
        for shelfName, products in sorted(mainShelf.items()):
            print(f"===Стеллаж {shelfName}")
            for product in products:
                idProduct, name, quantity, idOrder = product[0:4]
                print(f"{name} (id={idProduct})")
                print(f"заказ {idOrder}, {quantity} шт")
                if idProduct in additionalShelf:
                    print(f"доп стеллаж: {','.join(additionalShelf[idProduct])}")
                print()

        logger.info("Luck output console")
    except Exception as Ex:
        logger.error(f"Error output console {Ex}")