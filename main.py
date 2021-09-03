from selenium import webdriver
import time


driver = webdriver.Chrome(r"D:\chromedriver.exe")
driver.get("http://orteil.dashnet.org/experiments/cookie/")

cookie = driver.find_element_by_id("cookie")
items = driver.find_elements_by_css_selector("#store div")
item_ids = [item.get_attribute('id') for item in items]

timeout = time.time() + 10
five_min = time.time() + 60*5

while True:
    cookie.click()

    if time.time() > timeout:

        all_prices = driver.find_elements_by_css_selector("#store b")
        item_prices = []

        for price in all_prices:
            element_text = price.text
            if element_text != "":
                cost = int(element_text.split("-")[1].strip().replace(",", ""))
                item_prices.append(cost)

        cookie_upgrade = {}
        for n in range(len(item_prices)):
            cookie_upgrade[item_prices[n]] = item_ids[n]

        money_element = driver.find_element_by_id("money").text
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)

        affordable_upgrades = {}
        for cost, id in cookie_upgrade.items():
            if cookie_count > cost:
                affordable_upgrades[cost] = id

        highest_price_affordable_upgrade = max(affordable_upgrades)
        to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]

        driver.find_element_by_id(to_purchase_id).click()

        timeout = time.time() + 15

    if time.time() > five_min:
        cookie_per_s = driver.find_element_by_id("cps").text
        print(cookie_per_s)
        break
