from loguru import logger
from pydantic import BaseModel


class InventoryItem(BaseModel):
    """Class for keeping track of an item in inventory."""

    name: str
    product_id: str
    price: int

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
