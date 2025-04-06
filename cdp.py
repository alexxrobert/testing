"""Example of using CDP Mode without WebDriver"""
import asyncio
from contextlib import suppress
from seleniumbase import decorators
from seleniumbase.core import sb_cdp
from seleniumbase.undetected import cdp_driver


START_URL = \
    "https://www.leroymerlin.ro/produse/pereti-despartitori-si-tavane/477"


@decorators.print_runtime("CDP Priceline Example")
def main():
    url0 = "about:blank"  # Set Locale code from here first
    url1 = START_URL
    loop = asyncio.new_event_loop()
    driver = cdp_driver.cdp_util.start_sync()
    page = loop.run_until_complete(driver.get(url0))
    sb = sb_cdp.CDPMethods(loop, page, driver)
    sb.set_locale("en")  # This test expects English locale
    sb.open(url1)
    sb.sleep(2.5)
    sb.internalize_links()  # Don't open links in a new tab
    sb.sleep(3)
    sb.save_screenshot("now_secure_image.png")
    print("\nScreenshot saved to: %s\n" % "now_secure_image.png")


if __name__ == "__main__":
    with suppress(Exception):
        main()
