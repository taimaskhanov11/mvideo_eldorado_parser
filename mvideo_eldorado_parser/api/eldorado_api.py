from mvideo_eldorado_parser.api.base_store_api import BaseStoreApi

import asyncio

from loguru import logger

from mvideo_eldorado_parser.api.base_store_api import BaseStoreApi
from mvideo_eldorado_parser.api.models import InventoryItem
from mvideo_eldorado_parser.config.config import E_PRODUCT_IDS, CONFIG


class EldoradoApi(BaseStoreApi):
    """EldoradoApi"""

    async def get_items_data(self, product_ids=None):
        ids = ",".join(product_ids or self.product_ids)
        async with self.session.get(
                self.product_details_url,
                params=self.product_details_params | {"itemsIds": ids},
        ) as response:
            item_data = await response.json()
            return item_data

    async def get_item_objects(self, product_ids=None):
        logger.info(product_ids)
        items_data = await self.get_items_data(product_ids)
        logger.info(f"{self}| Получены цены и данные {items_data}")
        items_objs = {}
        for item_data in items_data:
            product_id: str = str(item_data["ItemId"])
            logger.debug(f"{self}| Создание товара {product_id}")
            name: str = item_data["Name"]
            price: int = item_data["Price"]
            sold_out: bool = item_data["IsAvailable"]
            url: str = item_data["Url"]
            item = self.create_item(product_id, name, price, sold_out, url)
            items_objs[product_id] = item
            logger.info(f"{self}| {item} Создан")
        return items_objs


ELDORADO_API = EldoradoApi(CONFIG['eldorado_api'], E_PRODUCT_IDS)
