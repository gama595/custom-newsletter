import logging
from importlib import reload


def setup_custom_logger():
    reload(logging)
    try:
        root_logger = logging.getLogger()
        # root_logger.setLevel(logging.INFO)
        root_logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler('app.log', 'a', 'utf-8')
        handler.setFormatter(logging.Formatter(
            '%(levelname)s: %(message)s'))
        root_logger.addHandler(handler)

    except Exception as e:
        logging.error(f'Logger - Erro ao personalizar logging: {e}')

    return logging
