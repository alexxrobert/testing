from seleniumbase import SB

START_URL = \
    "https://www.leroymerlin.ro/produse/pereti-despartitori-si-tavane/477/data.json"
with SB(uc=True, test=True, locale_code="en") as sb:
    sb.activate_cdp_mode(START_URL)
    sb.sleep(2.5)
    sb.uc_gui_click_captcha()
    sb.sleep(2.5)
    screenshot_path = "now_secure_image.png"
    sb.save_screenshot(screenshot_path)
    print("\nScreenshot saved to: %s\n" % screenshot_path)
