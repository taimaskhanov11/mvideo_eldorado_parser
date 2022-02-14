from selenium.webdriver import Chrome, Firefox
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


class FirefoxConfig:
    Service = FirefoxService
    Options = FirefoxOptions
    Manager = GeckoDriverManager
    Webdriver = Firefox


class ChromeConfig:
    Service = ChromeService
    Options = ChromeOptions
    Manager = ChromeDriverManager
    Webdriver = Chrome


class Driver:
    Chrome = ChromeConfig
    Firefox = FirefoxConfig
