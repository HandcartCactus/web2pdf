from selenium.webdriver.remote.webdriver import WebDriver


from abc import abstractmethod


class Adapter:
    def __init__(self):
        pass

    @abstractmethod
    def get_url(self, driver:WebDriver, url:str):
        pass

    @abstractmethod
    def get_page_content(self, driver:WebDriver):
        pass

    @abstractmethod
    def go_to_next_page(self, driver:WebDriver):
        pass

    @abstractmethod
    def has_more_content(self, driver:WebDriver):
        pass