from f_is_for_freedom.Adapter import Adapter


from PIL import Image
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


import time
from io import BytesIO


class DynamicLoadOnePagePngAdapter(Adapter):
    def __init__(self, page_content_xpath:str, next_page_xpath:str, load_delay:int=3) -> None:
        self.page_content_xpath = page_content_xpath
        self.next_page_xpath = next_page_xpath
        self.load_delay = load_delay

    def get_url(self, driver:WebDriver, url:str):
        driver.get(url=url)

    def get_page_content(self, driver:WebDriver):
        time.sleep(self.load_delay)

        # screenshot the content and split into pages
        content = driver.find_element(By.XPATH, self.page_content_xpath)
        img = Image.open(BytesIO(content.screenshot_as_png))
        return img

    def go_to_next_page(self, driver:WebDriver):
        driver.find_element(By.XPATH, self.next_page_xpath).click()

    def has_more_content(self, driver:WebDriver):
        has_more_content = False
        try:
            driver.find_element(By.XPATH, self.next_page_xpath)
            has_more_content = True
        except NoSuchElementException as e:
            pass

        return has_more_content