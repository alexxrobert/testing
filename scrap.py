from seleniumbase import DriverContext
from selenium.common.exceptions import NoSuchElementException
from sbvirtualdisplay import Display
import time
import csv
import os
SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

START_URL = "https://www.leroymerlin.ro/produse/pereti-despartitori-si-tavane/477"
OUTPUT_FILE = "screenshots/leroymerlin_products.csv"

def extract_products(driver):
    driver.wait_for_element("div.product-list", timeout=10)
    cards = driver.find_elements("css selector", "div.product-card")
    products = []

    for card in cards:
        try:
            name = card.find_element("css selector", ".product-title").text.strip()
            price = card.find_element("css selector", ".product-price .price-amount").text.strip()
            products.append((name, price))
        except Exception as e:
            print("⚠️ Skipping product due to error:", e)

    return products

def go_to_next_page(driver):
    try:
        next_button = driver.find_element("css selector", 'a[aria-label="Următoarea pagină"]')
        if "disabled" not in next_button.get_attribute("class"):
            driver.execute_script("arguments[0].scrollIntoView();", next_button)
            next_button.click()
            time.sleep(2)
            return True
    except NoSuchElementException:
        pass
    return False

def main():
    # Start SeleniumBase's virtual display (uses Xvfb)
    display = Display(visible=0, size=(1440, 1880))
    display.start()
    with DriverContext(uc=True, headless=False) as driver:
        driver.get(START_URL)

        all_products = []
        page_num = 1

        while True:
            print(f"🔍 Extracting page {page_num}...")
            time.sleep(2)
            screenshot_name = f"screenshot_page_{page_num}.png"
            screenshot_path = os.path.join(SCREENSHOT_DIR, screenshot_name)
            driver.save_screenshot(screenshot_path)
            print("\nScreenshot saved to: %s\n" % screenshot_path)
            products = extract_products(driver)
            all_products.extend(products)
            print(f"✅ Found {len(products)} products on page {page_num}")

            if not go_to_next_page(driver):
                break
            page_num += 1
            time.sleep(1)

        driver.quit()

        # Save to CSV
        with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Product Name", "Price"])
            writer.writerows(all_products)

        print(f"\n🎉 Done! Saved {len(all_products)} products to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
