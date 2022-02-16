from mvideo_eldorado_parser.api.base_store_api import BaseStoreApi

import asyncio

from loguru import logger

from mvideo_eldorado_parser.api.base_store_api import BaseStoreApi
from mvideo_eldorado_parser.api.models import InventoryItem
from mvideo_eldorado_parser.config.config import E_PRODUCT_IDS, CONFIG


class EldoradoApi(BaseStoreApi):
    """EldoradoApi"""

    async def get_items_data(self):
        ids = ",".join(self.product_ids)
        async with self.session.get(
                self.product_details_url,
                params=self.product_details_params | {"itemsIds": ids},
        ) as response:
            item_data = await response.json()
            return item_data

    async def get_prices(self) -> dict[str, int]:
        item_data = await self.get_items_data()
        item_prices = {}
        for item in item_data:
            item_id: str = item["ItemId"]
            price: int = item["Price"]
            item_prices[item_id] = price
        return item_prices

    async def _get_name_and_price(self, ) -> dict[str, tuple]:
        item_data = await self.get_items_data()
        item_prices = {}
        for item in item_data:
            name: str = item["Name"]
            item_id: str = item["ItemId"]
            price: int = item["Price"]
            item_prices[item_id] = name, price
        return item_prices

    async def create_items(self):
        """Получение данных и создание объектов"""
        items_data = await self._get_name_and_price()
        logger.info(f"{self}| Получены цены и данные {items_data}")
        for product_id, data in items_data.items():
            if product_id not in self.items:
                logger.debug(f"{self}| Создание товара {product_id}")
                item = await self.create_item(product_id, *data)
                await asyncio.sleep(self.delay_get_info)
                logger.info(f"{self}| {item} Создан")
                self.items[product_id] = item


ELDORADO_API = EldoradoApi(CONFIG['eldorado_api'], E_PRODUCT_IDS)
