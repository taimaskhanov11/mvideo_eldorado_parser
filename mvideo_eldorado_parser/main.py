import sys

from loguru import logger

from mvideo_eldorado_parser.config import CONFIG
from mvideo_eldorado_parser.parsing.driver import Driver
from mvideo_eldorado_parser.parsing.mvideo import StoreParser, StoreApi

logger.remove()
logger.add(sink=sys.stderr, level=CONFIG['log_level'], enqueue=True, diagnose=True, )
logger.add(sink=f"../logs/mainlog.log", level='TRACE', enqueue=True, encoding='utf-8', diagnose=True, )

if __name__ == '__main__':
    # DRIVER = getattr(Driver, CONFIG["WEBDRIVER"])
    # DRIVER_PATH = DRIVER.Manager().install()
    # store = StoreParser(CONFIG, DRIVER, DRIVER_PATH)
    # store.start()

    store_api = StoreApi(config=CONFIG)
    store_api.start()