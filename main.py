# Import Modules

from selenium import webdriver
# import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager
import requests
import os
import sys
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException


found = False


def run():
    chrome_options = webdriver.ChromeOptions()
    service = Service(executable_path=ChromeDriverManager().install())
    # chrome_options.add_argument('--proxy-server=socks5://52.157.88.150:80')
    # chrome_options.add_argument(f'--proxy-server={propro}')
    # driver = uc.Chrome(use_subprocess=True, chrome_options=chrome_options)
    # chrome_options.add_argument('headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", options=chrome_options)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 10)
    try:
        driver.get("https://mintle.app/explore/MANTLE:0x7cf4ac414c94e03ecb2a7d6ea8f79087453caef0")
        time.sleep(5)
        # input_tag = driver.find_element(By.XPATH, "//input[contains(@type, 'number')]")
        price_elm = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//input[contains(@type, 'number')]")))
        print(len(price_elm))
        price_elm[1].send_keys("9023")
        traits_elm = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//button[contains(@class, 'sc-iBkjds sc-ftvSup sc-hrZiYQ gYCGXc cLuCCY jCCGsr')]")))
        print(len(traits_elm))
        for elm in traits_elm:
            elm.click()
            parent_elm = (By.XPATH, "//div[contains(@class, 'sc-bczRLJ sc-gsnTZi IywNy ktCKzB')]")
            child_elm = (By.XPATH, "//span[contains(@class, 'sc-bjUoiL sc-idiyUo fMQLyS hJGsTm')]")
            all_filter = wait.until(EC.presence_of_all_elements_located((By.XPATH, ".//span[contains(@class, 'sc-bjUoiL sc-idiyUo fMQLyS hJGsTm')]")))
            for filters in all_filter:
                print(filters.text)
            print(all_filter)
            time.sleep(5)
        time.sleep(10)
        # get element
        # element = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[3]/div[3]/div[1]/button[2]")
        # element.click()
        # pw = driver.find_element(By.XPATH, "//input[@name='wallet_password']")
        # con_pw = driver.find_element(By.XPATH, "//input[@name='wallet_confirm_password']")
        # pw.send_keys("kopisaja")
        # con_pw.send_keys("kopisaja")
        # create = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[3]/div[4]/div[3]/button[1]")
        # create.click()
        # try:
        #     element = WebDriverWait(driver, 120).until(
        #         EC.presence_of_element_located((By.CLASS_NAME, "reapop__notification-message"))
        #     ).text
        #     print(element)
        #     if element == "Unable to reach faucet":
        #         driver.quit()
        #     else:
        #         print("faucet ready")
        #         time.sleep(7)
        #         sendDrop = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div[8]/div[1]/div[1]/button[1]")
        #         sendDrop.click()
        #         time.sleep(2)
        #         send = driver.find_element(By.XPATH,
        #                                    "/html/body/div[1]/div[1]/div[2]/div[8]/div[1]/div[1]/div[1]/ul[1]/li[3]/a[1]")
        #         send.click()
        #         time.sleep(2)
        #         address = driver.find_element(By.XPATH, "//input[@name='toAddress']")
        #         jml = driver.find_element(By.XPATH, "//input[@name='amount']")
        #         address.send_keys("")
        #         jml.send_keys("9.99")
        #         sendAct = driver.find_element(By.XPATH,
        #                                       "/html/body/div[1]/div[1]/div[2]/div[8]/div[1]/div[1]/div[1]/div[1]/div[3]/button[1]")
        #         sendAct.click()
        #         time.sleep(15)
        #         driver.quit()
        # finally:
        #     print("done")
    except WebDriverException:
        driver.quit()


run()

