from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

from contextlib import contextmanager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of

from pathlib import Path
import os
import shutil


SNAP_LOCATION = "/snap/bin/chromium.chromedriver"

def construct_headless_chrome_driver():
    options = ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")

    if os.path.exists(SNAP_LOCATION):
        path = SNAP_LOCATION
    else:
        path = shutil.which("chromedriver")
        assert path, "chromedriver not found. chromedriver must be installed."
    service = ChromeService(executable_path=path)

    return webdriver.Chrome(options=options, service=service)


def get_landing_page_url():
    test_dir = os.getcwd()
    index_path = os.path.join(test_dir, "..", "page", "index.html")
    index_uri = Path(index_path).as_uri()
    return index_uri


# As demonstrated in the linked web page from the course assignment
@contextmanager
def wait_for_page_load(driver, timeout=30):
    old_page = driver.find_element(By.TAG_NAME, 'html')
    yield
    WebDriverWait(driver, timeout).until( staleness_of(old_page) )

