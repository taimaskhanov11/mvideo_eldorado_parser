from pathlib import Path

import yaml

BASE_DIR = Path(__file__).parent.parent.parent

with open(Path(BASE_DIR, "config.yaml"), "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)


def get_product_ids():
    product_ids = []
    with open(Path(BASE_DIR, "product_ids.txt"), "r", encoding="utf-8") as f:
        for _id in f.readlines():
            _id = _id.strip()
            if _id:
                product_ids.append(_id)
    return product_ids


CONFIG = config
TG_TOKEN = CONFIG["TG_TOKEN"]
VERSION = CONFIG["VERSION"]
PRODUCT_IDS = get_product_ids()
ADMIN_IDS = CONFIG["ADMIN_IDS"]
