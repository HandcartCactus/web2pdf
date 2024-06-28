# web2pdf
Flexible utilities for turning multi-page websites into PDF documents for offline reading.
## Demo
The following code turns the website `https://www.example.com/multi-page-calculus-tutorial/` into an OCR'd PDF for later reading. The Website has multiple pages of varying length, with a significant number of images and diagrams. The `VariablePageSizePngAdapter` is a good choice. Using XPATH, we identify both the link to the next page `NEXT_PAGE_XPATH = '//div[@data-testid="NextPage"]/a'` and the XPATH for the main page content, which loads dynamically `PAGE_CONTENT_XPATH = '//section[@data-testid="DynamicPageContent"]'`. The code saves each page as a set of 8.5" x 11" images, then wraps them into an OCR'd PDF, and cleans up the images since they are no longer needed.
```python
from web2pdf.scrapers.InteractiveScraper import InteractiveScraper
from web2pdf.compilers.OcrPdfCompiler import OcrPdfCompiler
from web2pdf.storage.PngFsStorage import PngFsStorage
from web2pdf.adapters.VariablePageSizePngAdapter import VariablePageSizePngAdapter
from web2pdf.utils.make_driver import make_driver


# create an adapter for a specific website
class SomeAdapter(VariablePageSizePngAdapter):
    NEXT_PAGE_XPATH = '//div[@data-testid="NextPage"]/a'  # the xpath to the "next" link
    PAGE_CONTENT_XPATH = (
        '//section[@data-testid="DynamicPageContent"]'  # the xpath to the main contents
    )

    def __init__(self, load_delay: int = 3, pagedown_delay: int = 1) -> None:
        super().__init__(
            page_content_xpath=self.PAGE_CONTENT_XPATH,
            next_page_xpath=self.NEXT_PAGE_XPATH,
            load_delay=load_delay,
            pagedown_delay=pagedown_delay,
        )


if __name__ == "__main__":
    # selenium session, load our default browser profile so we look normal
    driver = make_driver(
        geckodriver_path="/path/to/geckodriver",
        profile_dir="path/to/.mozilla/firefox/sd98f7df.default-release",
        implicit_wait=2,
    )
    # create a basic scraper
    scraper = InteractiveScraper(
        driver=driver,
        adapter=SomeAdapter(),
        storage=PngFsStorage(
            "/dir/for/image/files"
        ),  # where to store intermediate image files
        compiler=OcrPdfCompiler(
            "/path/to/export/file.pdf"
        ),  # where to export final pdf
    )
    # actually do some scraping
    scraper("https://www.example.com/multi-page-calculus-tutorial/limits01.html")
    # remove unused image files
    storage.final_cleanup()
```

```
Paused. Begin Scraping? (Enter to continue):
Close Browser?  (y/n): y

...

OCR                   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 228/228 0:00:00
PDF/A conversion      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 228/228 0:00:00

Error: Invalid 0.0 horizontal text scaling given for Tz
Page 70
                 Output may be incorrect.

Linearizing           ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 100/100 0:00:00
Recompressing JPEGs   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   0% 0/0 -:--:--
Deflating JPEGs       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 190/190 0:00:00
JBIG2                 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   0% 0/0 -:--:--

```
