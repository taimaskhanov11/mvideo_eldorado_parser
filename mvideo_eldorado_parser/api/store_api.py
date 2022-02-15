import asyncio
import datetime
from dataclasses import dataclass

import aiohttp
from loguru import logger

from mvideo_eldorado_parser.app.bot import bot
from mvideo_eldorado_parser.config.config import ADMIN_IDS, CONFIG, PRODUCT_IDS


@dataclass
class InventoryItem:
    """Class for keeping track of an item in inventory."""

    name: str
    product_id: str
    price: int

    # def __str__(self):
    #     return f"{self.name}|{self.price:<8}"

    def __str__(self):
        return f"ID_{self.product_id:12}|{self.price:8}"

    def price_check(
        self, new_price
    ):  # todo 15.02.2022 21:11 taima: сделать что то с логами
        # print(type(new_price))
        if new_price == self.price:
            answer = f"{self} → {new_price:<8} [=]"
            logger.info(answer)

        elif new_price < self.price:
            answer = (f"{self} ↓ {new_price:<8} [✅]",)
            self.price = new_price
            logger.success(answer)

        else:
            answer = f"{self} ↑ {new_price:<8} [{'❌':5}]"
            self.price = new_price
            logger.warning(answer)

        return answer


class StoreApi:
    """StoreParserApi"""

    def __init__(self, config: dict, product_ids: list[str]):
        self.config = config
        self.headers = self.config["headers"]

        # self.session = requests.Session()
        # self.session.headers.update(headers)

        self.session: aiohttp.ClientSession = None

        self.product_prices_params = self.config["product_prices_params"]
        self.product_details_params = self.config["product_details_params"]

        self.product_prices_url = self.config["product_prices_url"]
        self.product_details_url = self.config["product_details_url"]

        self.product_ids: list = product_ids
        self.items: dict[str, InventoryItem] = {}

        self.delay_get_info = config["delay_get_info"]
        self.delay_get_prices = config["delay_get_prices"]

        self.items_changed = True

    async def get_info(self, product_id: str) -> dict:

        async with self.session.get(
            self.product_details_url,
            params=self.product_details_params | {"productId": product_id},
        ) as response:
            item_info = await response.json()
            return item_info

    async def get_name(self, product_id) -> str:
        item_info = await self.get_info(product_id)
        return item_info["body"]["name"]

    def del_old_items(self):
        for product_id in self.items.keys():
            if product_id not in self.product_ids:
                logger.warning(f"Удаление старого товара {self.items[product_id]}")
                del self.items[product_id]

    def clean_products(self):
        self.product_ids = []
        self.items = {}
        self.items_changed = True
        logger.info("Товары очищены!")

    def add_products(self, product_ids):
        self.product_ids.extend(product_ids)
        self.items_changed = True
        logger.info(f"Товары {product_ids} успешно добавлены")

    def delete_products(self, products_ids):
        for product_id in products_ids:
            if product_id in self.product_ids:
                logger.debug(f"Удаление {product_id} из списка")
                self.product_ids.remove(product_id)
                if product_id in self.items:
                    logger.debug(f"Удаление объекта {product_id} из списка")
                    del self.items[product_id]
        self.items_changed = True
        logger.info(f"Товары {products_ids} успешно удалены")

    async def create_items(self):
        prices = await self.get_price(self.product_ids)
        logger.info(f"Получены цены {prices}")

        for product_id, price in prices.items():
            if product_id not in self.items:
                logger.debug(f"Создание товара {product_id}")
                name = await self.get_name(product_id)
                await asyncio.sleep(self.delay_get_info)
                item = InventoryItem(name, product_id, price)
                logger.info(f"{item} Создан")
                self.items[product_id] = item

    async def get_price(self, ids: list[str]) -> dict[str, int]:
        ids = ",".join(ids)

        async with self.session.get(
            self.product_prices_url,
            params=self.product_prices_params | {"productIds": ids},
        ) as response:
            item_data = await response.json()
            item_prices = {}
            if item_data["success"] is True:
                items = item_data["body"]["materialPrices"]
                for item in items:
                    item_id: str = item["productId"]
                    price: int = item["price"]["salePrice"]
                    item_prices[item_id] = price
                return item_prices

            else:
                logger.critical(f"Ошибка при получении цен товаров {ids}")

    async def checking_price_changes(self):

        new_prices = await self.get_price(self.product_ids)
        results = [str(datetime.datetime.now())]
        for product_id, new_price in new_prices.items():
            item = self.items[product_id]
            res = item.price_check(new_price)
            results.append(res)
        str_results = "\n".join(results)
        await bot.send_message(ADMIN_IDS, str_results)

    def check_new_items(self):
        pass

    async def start(self):
        self.session = aiohttp.ClientSession(headers=self.headers)
        while True:
            logger.debug("Проверка изменения товаров")

            # проверка изменения товаров
            if self.items_changed:
                # удалить старые если имеются
                logger.debug("Удаление старых объектов товаров")
                self.del_old_items()

                logger.debug("Создание объектов товара и первоначальной стоимости")
                await self.create_items()
                self.items_changed = False

            logger.debug(f"Проверка стоимости товаров")
            await self.checking_price_changes()

            logger.debug(f"Сон на {self.delay_get_prices} sec")
            await asyncio.sleep(self.delay_get_prices)


STORE_API = StoreApi(config=CONFIG["store_api"], product_ids=PRODUCT_IDS)
