from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from typing import Optional


def make_driver(geckodriver_path:str, profile_dir:Optional[str]=None, implicit_wait:int=1, headless:bool=False):
    options = Options()
    options.headless = headless  # Change to True if you want to run headlessly
    options.profile = FirefoxProfile(profile_directory=profile_dir)

    service = Service(geckodriver_path)

    # Create a new instance of the Firefox driver
    driver = webdriver.Firefox(service=service, options=options)
    driver.implicitly_wait(implicit_wait)

    return driver