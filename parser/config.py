import os
import logging
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def get_driver(headless=False):
    options = Options()
    options.headless = headless

    driver_path = os.path.join(os.path.dirname(__file__), 'geckodriver')

    if not os.path.exists(driver_path):
        logging.error(
            "Geckodriver не найден по указанному пути: %s", driver_path)
        return None

    service = Service(executable_path=driver_path)

    try:
        driver = webdriver.Firefox(service=service, options=options)
        logging.info("Драйвер успешно создан.")
        return driver
    except Exception as e:
        logging.error("Ошибка при создании драйвера: %s", e)
        return None
