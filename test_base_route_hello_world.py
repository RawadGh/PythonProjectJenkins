import time
# from faker import Faker
import pytest
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FireFoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


@pytest.fixture()
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
        driver = webdriver.Remote("http://localhost:4444", desired_capabilities=dc, options=options)

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

    yield driver
    driver.close()


def test_status200(driver):
    driver.get("http://localhost:5000/stub")
    text_status200 = driver.find_element(By.XPATH, "/html/body").text
    assert "Value of Stub: 200" == text_status200

def test_displayed_text(driver):
    driver.get("http://localhost:5000/")
    text = driver.find_element(By.XPATH, "/html/body").text
    assert "Welcome to the Application with updated code!" == text


