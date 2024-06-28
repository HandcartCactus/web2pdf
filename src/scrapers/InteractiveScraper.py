from web2pdf.compilers.Compiler import Compiler
from web2pdf.storage.Storage import Storage
from web2pdf.adapters.Adapter import Adapter


from selenium.webdriver.remote.webdriver import WebDriver


class InteractiveScraper:
    def __init__(self, driver:WebDriver, adapter:'Adapter', storage:'Storage', compiler:'Compiler'):
        self.driver = driver
        self.adapter = adapter
        self.storage = storage
        self.compiler = compiler

    def confirm_continue(self, message:str):
        input(f'Paused. {message} (Enter to continue): ')

    def warn_exception(self, component:str, e:Exception):
        print("="*80)
        print(f"There was an issue: {component}")
        print(f"-"*80)
        print(e)
        print("="*80)

    def confirm_yesno(self, message:str):
        response = input(f"{message} (y/n): ")
        parsed = response.lower() == 'y'
        return parsed

    def __call__(self, url):
        self.storage.create_storage()

        self.adapter.get_url(self.driver, url)
        self.confirm_continue('Begin Scraping?')

        try:
            while True:
                page_content = None
                try:
                    page_content = self.adapter.get_page_content(self.driver)
                except Exception as e:
                    self.warn_exception('getting page content', e)
                    if not self.confirm_yesno('Continue Scraping?'):
                        raise e

                if page_content is not None:
                    try:
                        self.storage.save_page_content(page_content)
                    except Exception as e:
                        self.warn_exception('saving page content', e)
                        if not self.confirm_yesno('Continue Scraping?'):
                            raise e

                try:
                    if self.adapter.has_more_content(self.driver):
                        self.adapter.go_to_next_page(self.driver)
                    else:
                        break
                except Exception as e:
                        self.warn_exception('going to the next page', e)
                        if not self.confirm_yesno('Continue Scraping?'):
                            raise e
        except Exception as e:
            self.warn_exception('main loop', e)
            if not self.confirm_yesno('Compile Content?'):
                raise e
        finally:
            self.confirm_continue('Close Browser?')
            try:
                self.driver.close()
            except Exception as e:
                pass

        result = self.compiler.compile_content(self.storage.all_content())
        return result
