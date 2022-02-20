from loguru import logger
from pydantic import BaseModel


class CheckItem(BaseModel):
    product_id: str
    price: int
    sold_out: bool


class InventoryItem(BaseModel):
    """Class for keeping track of an item in inventory."""

    product_id: str
    name: str
    price: int
    sold_out: bool
    url: str

    def __str__(self):
        # return f"ID_{self.product_id:12}|{self.price:8}"
        return f"ID_{self.name:12}|{self.url} | "

    def pretty(self):
        return f"__[{self.product_id}]__\n{self.name}\n{self.url}\nЦена: {self.price}\nВ продаже: {self.sold_out}"

    def find_differences(self, item: "InventoryItem") -> str:
        result = ""
        price_diff = self.price_check(item.price)
        sold_out_diff = self.sold_out_check(item.sold_out)
        if any((price_diff, sold_out_diff)):
            result = f"{price_diff}\n{sold_out_diff}"
        return result

    # todo 17.02.2022 22:11 taima:

    def sold_out_check(self, new_status: bool):
        answer = f"{self}{self.sold_out}"
        diff = False
        if self.sold_out is True:
            if new_status is False:
                answer += f" → {new_status} [❌] Больше не в продаже!"
                self.sold_out = new_status
                logger.info(f"answer")
                diff = True

        elif self.sold_out is False:
            if new_status is True:
                answer += f" → {new_status} [✅] Появилась в продаже!"
                self.sold_out = new_status
                logger.info(f"answer")
                diff = True

        return answer if diff else ""

    def price_check(
        self, new_price
    ):  # todo 15.02.2022 21:11 taima: сделать что то с логами
        # print(type(new_price))
        answer = f"{self}{self.price} "
        diff = False
        if new_price == self.price:
            answer += f"→ {new_price:<8} [=]"
            logger.info(answer)

        elif new_price < self.price:
            answer += f"↓ {new_price:<8} [✅] Цена упала!"
            self.price = new_price
            logger.success(answer)
            diff = True
        else:
            answer += f"↑ {new_price:<8} [{'❌':5}] Цена Повысилась!"
            self.price = new_price
            logger.warning(answer)
            diff = True

        return answer if diff else ""
