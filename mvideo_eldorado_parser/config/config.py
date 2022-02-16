import os
from pathlib import Path

import yaml

BASE_DIR = Path(__file__).parent.parent.parent
CONFIG_FILE = os.getenv("CONFIG_FILE") or "config.yaml"

with open(Path(BASE_DIR, CONFIG_FILE), "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)


def get_product_ids():
    product_ids = []
    for file in ["m_product_ids.txt", "e_product_ids.txt"]:
        ids = []
        with open(Path(BASE_DIR, file), "r", encoding="utf-8") as f:
            for _id in f.readlines():
                _id = _id.strip()
                if _id:
                    ids.append(_id)
        product_ids.append(ids)
    return product_ids


CONFIG = config
TG_TOKEN = CONFIG["TG_TOKEN"]
VERSION = CONFIG["VERSION"]
M_PRODUCT_IDS, E_PRODUCT_IDS = get_product_ids()
ADMIN_IDS = CONFIG["ADMIN_IDS"]
