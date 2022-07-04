import time
from faker import Faker
import pytest
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FireFoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


@pytest.fixture() #11
def driver():
    firefox_driver_binary = "./drivers/geckodriver"
    ser_firefox = FirefoxService(firefox_driver_binary)
    firefox_options = FireFoxOptions()


    chrome_path = "./drivers/chromedriver"
    options = webdriver.ChromeOptions()
    options.binary_location = chrome_path

    browser_name = "firefox"

    # if isinstance(browserName,list):
    #     for browser_name in browserName:
    if browser_name == "firefox-webdriver":
        driver = webdriver.Firefox(service=ser_firefox)
    elif browser_name == "firefox":
        firefox_options.add_argument("--headless")
        dc = {
            "browserName": "firefox",
            "platformName": "Windows 11"
        }
        driver = webdriver.Remote("http://localhost:4444", desired_capabilities=dc, options=firefox_options)

    elif browser_name == "chrome":
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")

        dc = {
            "browserName": "chrome",
            "platformName": "Windows 11"
        }
        driver = webdriver.Remote("http://localhost:4444", desired_capabilities=dc, options=options)

    elif browser_name == "edge":
        options.add_argument("--headless")
        dc = {
            "browserName": "MicrosoftEdge",
            "platformName": "Windows 11"
        }
        driver = webdriver.Remote("http://localhost:4444", desired_capabilities=dc , options=options)

    elif browser_name == "firefox-mobile":
        firefox_options = FireFoxOptions()
        firefox_options.add_argument("--width=375")
        firefox_options.add_argument("--height=812")
        firefox_options.set_preference("general.useragent.override", "userAgent=Mozilla/5.0 "
                                                                     "(iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like "
                                                                     "Gecko) CriOS/101.0.4951.44 Mobile/15E148 Safari/604.1")
        # firefox_options.set_preference("general.useragent.override", "Nexus 7")

        driver = webdriver.Firefox(service=ser_firefox, options=firefox_options)

    elif browser_name == "android-emulator":
        dc = {
            "platformName": "Android",
            "platformVersion": "8.1.0",
            "deviceName": "Android Emulator",
            # "platformVersion": "11.0.0",
            # "deviceName": "1aaa4ea80404",
            "automationName": "Appium",
            # "app": "com.android.chrome",
            "browserName": "Chrome"
        }
        driver = webdriver.Remote("http://localhost:4723/wd/hub", dc)

    elif browser_name == "android-phone":
        dc = {
            "platformName": "Android",
            "platformVersion": "11.0.0",
            "deviceName": "1aaa4ea80404",
            "automationName": "Appium",
            "browserName": "Chrome"
        }

        driver = webdriver.Remote("http://localhost:4723/wd/hub", dc)
    else:
        raise Exception("driver doesn't exists")

    # firefox_options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')

    # capabilities = {
    #     'browserName': 'firefox',
    #     'firefoxOptions': {
    #         'mobileEmulation': {
    #             'deviceName': 'iPhone X'
    #         }
    #     }
    # }
    # user_agent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16"

    # profile = webdriver.FirefoxProfile()
    # profile.set_preference("general.useragent.override", user_agent)
    # driver = webdriver.Firefox(profile)

    # parent_handle = driver.current_window_handle
    # for handle in driver.window_handles:
    #     if parent_handle != handle:
    #         driver.switch_to(handle)

    yield driver
    driver.close()


# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# chrome_options = Options()
# chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
# driver = webdriver.Chrome(chrome_options = chrome_options)


def test_testPositiveRegistration(driver):
    driver.get("https://www.urbanica-wh.com/")
    driver.maximize_window()
    driver.find_element(By.ID, "customer-login-link").click()
    time.sleep(10)
    driver.find_element(By.CSS_SELECTOR, "#customer-popup-registration > span").click()
    driver.find_element(By.ID, "firstname").send_keys("rawad")
    driver.find_element(By.ID, "lastname").send_keys("ghname")
    fake = Faker()
    proper_email = fake.ascii_email()
    driver.find_element(By.ID, "register_email_address").send_keys(proper_email)
    driver.find_element(By.ID, "register_password").send_keys("Vd89651**")
    driver.find_element(By.CSS_SELECTOR, ".label:nth-child(2) > span").click()
    driver.find_element(By.CSS_SELECTOR, ".actions-toolbar-submit:nth-child(1) span").click()
    time.sleep(15)
    driver.find_element(By.CSS_SELECTOR, "#customer-account-link").click()
    time.sleep(5)
    assert driver.find_element(By.CSS_SELECTOR,
                                        "#ui-id-5 > div.block-title.customer-name > span").text == 'היי, rawad'




def test_google_page_title(driver):
    driver.get('https://www.google.com')
    title = driver.title
    driver.save_screenshot("test_google_page_title.png")
    assert title == str.title("google")


# def test_youtube_page_title(driver):
#     driver.get('https://www.youtube.com')
#     title = driver.title
#     assert title == "Home - YouTube"
#
#
# def test_addition_of_2_and_5_simple(driver):
#     driver.get('https://www.google.com')
#     # css_selector, xpath
#     search_field = driver.find_element(By.NAME, "q")
#     search_field.click()
#     search_field.send_keys("2 + 5")
#     search_field.send_keys(Keys.ENTER)
#
#     ans_selector = "#cwos"
#
#     # WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,ans_selector)))
#     # actual_field = driver.find_element(By.CSS_SELECTOR,ans_selector)
#
#     actual_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ans_selector)))
#
#     assert actual_field.text == str(7)
#
#     time.sleep(3)
#
#
# calc_numbers_input = [("2 + 5", 7), ("3 + 6", 9), ("12 + -1", 11), ("6*9", 40)]
# message_for_calc_numbers_input = [f"Testing {expected} = {ans}" for expected, ans in calc_numbers_input]
#
#
# @pytest.mark.parametrize(
#     "test_input,expected_output",
#     [("2 + 5", 7), ("3 + 6", 9), ("12 + -1", 11), ("6*9", 40)],
#     ids=message_for_calc_numbers_input
# )
# def test_addition_of_2_and_5(driver, test_input, expected_output):
#     driver.get('https://www.google.com')
#     # css_selector, xpath
#     search_field = driver.find_element(By.NAME, "q")
#     search_field.click()
#     search_field.send_keys(test_input)
#     search_field.send_keys(Keys.ENTER)
#
#     ans_selector = "#cwos"
#
#     # WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,ans_selector)))
#     # actual_field = driver.find_element(By.CSS_SELECTOR,ans_selector)
#
#     actual_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ans_selector)))
#
#     assert actual_field.text == str(expected_output)
#
#     time.sleep(3)
#
#
# def test_youtube_search_and_play_video(driver):
#     driver.get("https://www.youtube.com/")
#     search_field = driver.find_element(By.NAME, "search_query")
#     search_option_selector = "ytd-video-renderer.ytd-item-section-renderer:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > h3:nth-child(1) > a:nth-child(2) > yt-formatted-string:nth-child(2)"
#     search_field.click()
#     time.sleep(1)
#     search_field.send_keys("testing qa automation")
#     search_field.send_keys(Keys.ENTER)
#
#     first_elem = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, search_option_selector)))
#
#     if first_elem:
#         driver.execute_script("window.scrollTo(0, window.scrollY + 200)")
#
#     first_elem.click()
#
#     first_elem_video_selector = ".video-stream"
#     first_elem_video = WebDriverWait(driver, 10) \
#         .until(EC.presence_of_element_located((By.CSS_SELECTOR, first_elem_video_selector)))
#     time.sleep(4)
#
#     first_elem_video.click()
#
#     first_elem_video_title_selector = "yt-formatted-string.ytd-video-primary-info-renderer:nth-child(1)"
#     first_elem_video_title = WebDriverWait(driver, 10) \
#         .until(EC.presence_of_element_located((By.CSS_SELECTOR, first_elem_video_title_selector)))
#
#     assert first_elem_video_title.text == "What is Automated Testing?"
#
#     time.sleep(5)

#
# def test_run_parallel(browserName):
#     if isinstance(browserName, list):
#         threads = []
#         for i, browser in enumerate(browserName):
#             thread = Thread(target=test_google_page_title, args=[browser])
#             threads.append(thread)
#             thread.start()
# #
#         for thread in threads:
#             thread.join()
#
#     print("all browsers ready")


# for i, b in enumerate(test_google_page_title):
#     print ("browser %s's title: %s" % (b["data"]["name"], b["driver"].title))
#     b["driver"].quit()
