import yaml

from mvideo_eldorado_parser.parsing.driver import Driver

with open("../config.yaml", "r", encoding="utf-8") as f:
    CONFIG = yaml.safe_load(f)


