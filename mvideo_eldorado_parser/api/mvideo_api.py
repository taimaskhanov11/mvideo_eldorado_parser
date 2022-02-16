import asyncio

from loguru import logger

from mvideo_eldorado_parser.api.base_store_api import BaseStoreApi
from mvideo_eldorado_parser.api.models import InventoryItem
from mvideo_eldorado_parser.config.config import CONFIG, M_PRODUCT_IDS


class MvideoApi(BaseStoreApi):
    """MvideoApi"""

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

    async def get_prices(self) -> dict[str, int]:
        ids = ",".join(self.product_ids)
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
            logger.critical(f"{self}| Ошибка при получении цен товаров {self.product_ids}")

    async def create_items(self):
        """Получение данных и создание объектов"""
        prices = await self.get_prices()
        logger.info(f"{self}| Получены цены {prices}")

        for product_id, price in prices.items():
            if product_id not in self.items:
                logger.debug(f"{self}| Создание товара {product_id}")
                name = await self.get_name(product_id)
                item = await self.create_item(product_id, name, price)
                await asyncio.sleep(self.delay_get_info)
                logger.info(f"{self}| {item} Создан")


MVIDEO_API = MvideoApi(CONFIG["mvideo_api"], M_PRODUCT_IDS)
