from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests, re, json, os, sys, time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException


all_nft_data = {}


def send_to_telegram():
    global all_nft_data
    token = 'replace_token'
    apiURL = 'https://api.telegram.org/bot'+token+'/sendMessage'
    try:
        response = requests.post(apiURL, json={'chat_id': replace_chatid, 'text': all_nft_data})
    except Exception as e:
        print(e)


def get_filter():
    url = ''
    resp = requests.get(url)
    data_filter = resp.json()
    print(data_filter)
    with open('filter.json', 'w') as json_file:
        json.dump(data_filter, json_file, indent=2)


def get_all_nft(driver):
    global all_nft_data
    try:
        time.sleep(5)
        count = 0
        all_nft = driver.find_elements(By.XPATH, "//span[@data-anchor='item-title']")
        for nft in all_nft:
            if nft.text not in all_nft_data:
                price = driver.execute_script(
                    "return arguments[0].parentNode.parentNode.parentNode.nextElementSibling.querySelector('span.sc-bjUoiL.sc-idiyUo.fMQLyS.hJGsTm').textContent;",
                    nft)
                link = driver.execute_script(
                    "return arguments[0].parentNode.parentNode.parentNode.parentNode.parentNode.href;",
                    nft)
                # print("Name: ", nft.text, price, link)
                # if count % 4 == 0:
                all_nft_data[nft.text] = link
                if nft == all_nft[-1]:
                    driver.execute_script("arguments[0].scrollIntoView();", nft)
                    time.sleep(2)
                    get_all_nft(driver)

            count += 1
    except WebDriverException as e:
        print(e)
        driver.quit()


def run():
    filter_list = ["Status", "Price", "BACKGROUND", "EYE", "EYEBROW", "HAIR", "HAND", "HEADGEAR", "MOUTH", "OUTFIT",
                   "RARE_HAIR", "SKIN"]
    data_filter = json.load(open("filter.json"))
    filter_price = data_filter["price"]
    filter_trait = data_filter["filter"]
    # print(filter_trait)
    chrome_options = webdriver.ChromeOptions()
    service = Service(executable_path=ChromeDriverManager().install())
    # chrome_options.add_argument('headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    try:
        driver.get("https://mintle.app/explore/MANTLE:0x7cf4ac414c94e03ecb2a7d6ea8f79087453caef0")
        time.sleep(5)
        # close cookie btn
        cookie_btn = driver.find_element(By.XPATH, "//*[@id='root']/div[2]/button")
        if cookie_btn:
            cookie_btn.click()
        price_elm = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//input[contains(@type, 'number')]")))
        # set lowest price
        price_elm[0].send_keys(filter_price["lowest"])
        # set highest price
        price_elm[1].send_keys(filter_price["highest"])
        # get all filter elements
        traits_elm = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//button[contains(@class, 'sc-iBkjds sc-ftvSup sc-hrZiYQ gYCGXc cLuCCY jCCGsr')]")))
        count = 0
        for elm in traits_elm:
            if count > 1 and filter_list[count] in filter_trait:
                # print(filter_list[count], filter_trait[filter_list[count]])
                filter = filter_list[count] + "-filter"
                filter_scroll = filter_list[count - 1] + "-filter"
                # print(filter_scroll)
                # scroll element to last filter
                if filter_scroll != "HAND-filter" and filter_scroll != "OUTFIT-filter":
                    driver.execute_script("arguments[0].scrollIntoView();",
                                          driver.find_element(By.XPATH, "//div[@data-testid='" + filter_scroll + "']"))
                elm.click()
                time.sleep(1)
                child_elm = driver.find_elements(By.XPATH,
                                                 "//div[@data-testid='" + filter + "']/div/div/div/div[*]/button/div/span/div/span")
                for c in child_elm:
                    if c.text in filter_trait[filter_list[count]]:
                        driver.execute_script("arguments[0].scrollIntoView();", c)
                        driver.execute_script(
                            "return arguments[0].parentNode.parentNode.parentNode.parentNode.click();", c)

                    if c.text not in filter_trait[filter_list[count]] and c == child_elm[-1]:
                        driver.execute_script("arguments[0].scrollIntoView();", c)
                time.sleep(2)

            count += 1

        # apply all filter
        apply_elm = driver.find_element(By.XPATH,
                                        "//*[@id='root']/div/div/div/div[3]/div/div/div[1]/div/div/div[1]/div/div/div[3]/div/div[1]/button")
        driver.execute_script("arguments[0].scrollIntoView();", apply_elm)
        apply_elm.click()
        # start scraping all nft
        time.sleep(2)
        get_all_nft(driver)
        send_to_telegram()
        time.sleep(5)
        driver.quit()
    except WebDriverException as e:
        driver.quit()


get_filter()
run()
