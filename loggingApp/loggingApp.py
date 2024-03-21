# Модуль для настройки логгирования
# Создает два логгера - для информационных и для ошибочных сообщений

import logging

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Настройка формата вывода логов
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Настройка вывода логов с уровнем INFO и выше в один файл
info_file_handler = logging.FileHandler('loggingApp\info.log')
info_file_handler.setLevel(logging.INFO)
info_file_handler.setFormatter(formatter)
logger.addHandler(info_file_handler)

# Настройка вывода логов с уровнем ERROR и выше в другой файл
error_file_handler = logging.FileHandler('loggingApp\error.log')
error_file_handler.setLevel(logging.ERROR)
error_file_handler.setFormatter(formatter)
logger.addHandler(error_file_handler)


if __name__ == "__main__":
    logging.info('Info')
    logging.error('Error')
