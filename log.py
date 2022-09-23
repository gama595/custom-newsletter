import logging
from importlib import reload


def setup_custom_logger():
    reload(logging)

    root_logger = logging.getLogger()
    # root_logger.setLevel(logging.INFO)
    root_logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler('app.log', 'a', 'utf-8')
    handler.setFormatter(logging.Formatter(
        '%(levelname)s: %(message)s'))
    root_logger.addHandler(handler)

    return logging
