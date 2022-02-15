import json
import re
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

import requests
from loguru import logger
from selenium.webdriver import Chrome, Firefox
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from .driver import ChromeConfig, FirefoxConfig


class Elements:
    TITLE_TAG = "h1"
    PRICE_CLASS = "price__main-value"
    PRICE_XPATH = "//span[@_ngcontent-serverapp-c106]"
    MINI_PRICE_CLASS = ""


class BaseStoreParser(ABC):
    """FooClass"""

    def __init__(
        self,
        config: dict,
        driver: FirefoxConfig | ChromeConfig,
        driver_path: str,
    ):
        self.config = config
        self.driver = driver
        self.driver_path = driver_path

        service = self.driver.Service(
            self.driver_path, log_path=str(Path("../logs", "geckodriver.log"))
        )

        options: FirefoxOptions | ChromeOptions = self.driver.Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument(
            f"user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1"
        )

        if self.config["headless"]:
            options.add_argument("--headless")

        self.driver: Chrome | Firefox = self.driver.Webdriver(
            service=service, options=options
        )
        self.delay = self.config["delay"]
        self.wait_for_delay = self.config["wait_for_delay"]
        # self.driver.set_window_size(500, 600)

        self.driver.maximize_window()

    def get(self, url):
        self.driver.get(url)

    def new_tab(self, url):
        self.driver.execute_script(f"""window.open("{url}","_blank");""")

    def switch_to(self, tab):
        self.driver.switch_to.window(tab)

    def sleep(self, s=0):
        time.sleep(self.delay + s)

    def _load_cookies(self, cookies_path):
        with open(cookies_path, "r") as f:
            cookies: list = json.load(f)

        for cookie in cookies:
            self.driver.add_cookie(cookie)

    def _save_cookies(self, data, path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)

    def wait_for(
        self, by: str, value: str, second: int = None, driver: Chrome | Firefox = None
    ):
        res = WebDriverWait(driver or self.driver, second or self.wait_for_delay).until(
            expected_conditions.presence_of_element_located((by, value))
        )
        return res

    @abstractmethod
    def start(self):
        pass


class StoreParser(BaseStoreParser):
    """ParsingSelenium"""

    def __init__(
        self,
        config: dict,
        driver: FirefoxConfig | ChromeConfig,
        driver_path: str,
    ):
        super().__init__(config, driver, driver_path)

        self.home_page = "https://www.mvideo.ru"
        self.item_page = config["item_page"]
        self.item_codes: list = config["item_codes"]
        self.items: list[InventoryItem] = []

    def get_price(self):
        price_: str = self.wait_for(By.CLASS_NAME, Elements.PRICE_CLASS).text
        price = int("".join(re.findall(r"\d", price_)))
        return price

    def get_title(self):
        return self.wait_for(By.TAG_NAME, Elements.TITLE_TAG).text

    def create_item(self, code: int, url: str):
        title = self.get_title()
        logger.trace(title)
        price = self.get_price()
        logger.trace(title)
        item = InventoryItem(title, code, url, price)
        logger.info(f"Товар {item} успешно создан!")
        self.items.append(item)

    def create_tabs_and_create_items(self):
        for code in self.item_codes:
            url = f"{self.item_page}{code}"
            self.new_tab(url)
            # self.sleep(300)
            logger.trace(f"Создание товара [{url}]{self.driver.current_url}")
            self.create_item(code, url)
        self.driver.close()

    def checking_price_changes(self):
        tabs = self.driver.window_handles
        tabs.reverse()
        for num, tab in enumerate(tabs):
            logger.trace(num)
            self.switch_to(tab)
            self.driver.refresh()
            item = self.items[num]
            logger.trace(self.driver.current_url)
            logger.debug(f"Проверка изменения цены {item}")
            # new_price = self.get_price()
            # logger.trace(new_price)
            # item.price_check(new_price)
            self.sleep(5)

    def start(self):
        logger.info("Запуск скрипта")
        try:
            logger.debug("Переход на главную страницу")
            self.get(self.home_page)
            logger.debug("Создание вкладок и товаров")
            # self.sleep(300)
            self.create_tabs_and_create_items()
            self.checking_price_changes()
        # except Exception as e:
        #     logger.error(e)
        #     raise e
        finally:
            logger.debug("Закрытие скрипта")
            # self.sleep(300)
            self.driver.quit()
            logger.info("Скрипт успешно закрыт")
