import asyncio
import datetime
from abc import ABC, abstractmethod
from typing import Optional

import aiohttp
from loguru import logger

from mvideo_eldorado_parser.api.models import InventoryItem
from mvideo_eldorado_parser.app.bot import bot
from mvideo_eldorado_parser.config.config import ADMIN_IDS


class BaseStoreApi(ABC):
    """StoreParserApi"""

    def __init__(self, config: dict, product_ids: list[str]):
        self.config = config
        self.headers = self.config["headers"]
        self.session: Optional[aiohttp.ClientSession] = None

        self.product_prices_params = self.config["product_prices_params"]
        self.product_details_params = self.config["product_details_params"]

        self.product_prices_url = self.config["product_prices_url"]
        self.product_details_url = self.config["product_details_url"]

        self.product_ids: list = product_ids
        self.items: dict[str, InventoryItem] = {}

        self.delay_get_info = config["delay_get_info"]
        self.delay_get_prices = config["delay_get_prices"]

        self.launch_status = False
        self.items_changed = True

    def __str__(self):
        return self.__class__.__name__

    @property  # todo 16.02.2022 23:33 taima: доработать
    def pretty_items(self):
        res = f"[{self}]\n"
        for item in self.items.values():
            res += f"{item.name} "
        return res

    def del_old_items(self):
        for product_id in self.items.keys():
            if product_id not in self.product_ids:
                logger.warning(f"{self}| Удаление старого товара {self.items[product_id]}")
                del self.items[product_id]

    def clean_products(self):
        self.product_ids = []
        self.items = {}
        self.items_changed = True
        logger.info(f"{self}| Товары очищены!")

    def add_products(self, product_ids):
        self.product_ids.extend(product_ids)
        self.items_changed = True
        logger.info(f"{self}| Товары {product_ids} успешно добавлены")

    def delete_products(self, products_ids):
        for product_id in products_ids:
            if product_id in self.product_ids:
                logger.debug(f"{self}| Удаление {product_id} из списка")
                self.product_ids.remove(product_id)
                if product_id in self.items:
                    logger.debug(f"{self}| Удаление объекта {product_id} из списка")
                    del self.items[product_id]
        self.items_changed = True
        logger.info(f"{self}| Товары {products_ids} успешно удалены")

    @abstractmethod
    async def get_prices(self) -> dict[str, int]:
        """Получение цены товара"""

    async def create_item(self, product_id, name, price) -> InventoryItem:
        """Создание объектов товара"""
        item = InventoryItem(name=name, product_id=product_id, price=price)
        self.items[product_id] = item
        return item

    @abstractmethod
    async def create_items(self):
        """Получение данных и создание объектов"""

    async def checking_price_changes(self):
        new_prices = await self.get_prices()
        results = [f"[{self}] | {datetime.datetime.now().replace(microsecond=0)}\n"]
        for product_id, new_price in new_prices.items():
            item = self.items[product_id]
            res = item.price_check(new_price)
            results.append(res)
        str_results = "\n".join(results)
        for user_id in ADMIN_IDS:
            await bot.send_message(user_id, str_results)

    async def start(self):
        self.launch_status = True
        self.session = aiohttp.ClientSession(headers=self.headers)
        while True:

            logger.debug(f"{self}| Проверка статус запуска")
            if self.launch_status is False:
                logger.info(f"{self}| Выключен. Ожидание 10 сек")
                await asyncio.sleep(10)
                continue

            logger.debug(f"{self}| Проверка изменения товаров")
            # проверка изменения товаров
            if self.items_changed:
                # удалить старые если имеются
                logger.debug(f"{self}| Удаление старых объектов товаров")
                self.del_old_items()

                logger.debug(f"{self}| Создание объектов товара и первоначальной стоимости")
                await self.create_items()
                self.items_changed = False

            logger.debug(f"{self}| Проверка стоимости товаров")
            await self.checking_price_changes()

            logger.debug(f"{self}| Сон на {self.delay_get_prices} sec")
            await asyncio.sleep(self.delay_get_prices)
