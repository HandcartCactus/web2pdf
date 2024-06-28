from f_is_for_freedom.Adapter import Adapter


from PIL import Image
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver


import time
from io import BytesIO
from math import ceil


class VariablePageSizePngAdapter(Adapter):
    BODY_XPATH = '//body'
    PAGE_ASPECT_RATIO = 11.0/8.5
    def __init__(self, page_content_xpath:str, next_page_xpath:str, load_delay:int=3, pagedown_delay:int=1) -> None:
        self.page_content_xpath = page_content_xpath
        self.next_page_xpath = next_page_xpath
        self.load_delay = load_delay
        self.pagedown_delay = pagedown_delay

    def get_url(self, driver:WebDriver, url:str):
        driver.get(url=url)

    def get_page_content(self, driver:WebDriver):
        page_content = []

        # let page load
        time.sleep(self.load_delay)

        # load full page by scrolling all the way down to the bottom
        driver.find_element(By.XPATH, self.BODY_XPATH).send_keys(Keys.END)
        driver.find_element(By.XPATH, self.BODY_XPATH).send_keys(Keys.HOME)

        # screenshot the content and split into pages
        content = driver.find_element(By.XPATH, self.page_content_xpath)
        img = Image.open(BytesIO(content.screenshot_as_png))
        w, h = img.size
        slice_h = int(w * self.PAGE_ASPECT_RATIO)
        n_pages = ceil(h/slice_h)
        for page_idx in range(n_pages):

            upper_px = slice_h * page_idx
            lower_px = min(upper_px + slice_h, h)
            page_content.append(img.crop((0, upper_px, w, lower_px)))

            # simulate reading
            driver.find_element(By.XPATH, self.BODY_XPATH).send_keys(Keys.PAGE_DOWN)
            time.sleep(self.pagedown_delay)

        return page_content

    def go_to_next_page(self, driver:WebDriver):
        driver.find_element(By.XPATH, self.BODY_XPATH).send_keys(Keys.END)
        driver.find_element(By.XPATH, self.next_page_xpath).click()

    def has_more_content(self, driver:WebDriver):
        has_more_content = False
        driver.find_element(By.XPATH, self.BODY_XPATH).send_keys(Keys.END)
        try:
            driver.find_element(By.XPATH, self.next_page_xpath)
            has_more_content = True
        except NoSuchElementException as e:
            pass

        return has_more_content