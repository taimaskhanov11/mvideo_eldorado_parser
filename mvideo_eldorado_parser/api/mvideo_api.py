import asyncio
from pprint import pprint

from loguru import logger

from mvideo_eldorado_parser.api.base_store_api import BaseStoreApi
from mvideo_eldorado_parser.api.models import InventoryItem
from mvideo_eldorado_parser.config.config import CONFIG, M_PRODUCT_IDS


class MvideoApi(BaseStoreApi):
    """MvideoApi"""

    async def get_item_data(self, product_id: str) -> dict:
        async with self.session.get(
                self.product_details_url,
                params=self.product_details_params | {"productId": product_id},
        ) as response:
            try:
                item_info = await response.json() #todo 19.02.2022 13:04 taima:
            except Exception as e:
                await response.text()
                logger.critical(e)
                raise e
            return item_info

    async def get_item_fields(self, product_id) -> tuple:
        item_info = await self.get_item_data(product_id)
        name: str = item_info["body"]["name"]
        sold_status: bool = not item_info["body"]["status"]["soldOut"]
        url: str = f"{self.product_url}{product_id}"
        return name, sold_status, url

    async def get_item_objects(self, product_ids=None) -> dict[str, InventoryItem]:
        prices = await self.get_prices(product_ids or self.product_ids)
        logger.info(f"{self}| Получены цены {prices}")
        items_objs = {}
        for product_id, price in prices.items():
            logger.debug(f"{self}| Создание товара {product_id}")
            name, sold_out, url = await self.get_item_fields(product_id)
            logger.info(f"{self}| полученны данные {name, sold_out, url} ")
            item = self.create_item(product_id, name, price, sold_out, url)
            logger.info(f"{self}| {item} Создан")
            items_objs[product_id] = item
        return items_objs

    async def get_prices(self, product_ids=None) -> dict[str, int]:
        ids = ",".join(product_ids or self.product_ids)
        item_prices = {}
        if ids:
            logger.info(ids)
            async with self.session.get(
                    self.product_prices_url,
                    params=self.product_prices_params | {"productIds": ids},
            ) as response:
                item_data = await response.json()
            logger.trace(f"{self}| Получение цен!| {item_data}")
            # pprint(item_data)
            # if item_data["success"] is True:
            items = item_data["body"]["materialPrices"]
            for item in items:
                item_id: str = item["productId"]
                price: int = item["price"]["salePrice"]
                item_prices[item_id] = price
            logger.info(item_prices)
        return item_prices
        # else:
        #     logger.critical(f"{self}| Ошибка при получении цен товаров {self.product_ids}")


MVIDEO_API = MvideoApi(CONFIG["mvideo_api"], M_PRODUCT_IDS)
