
from time import sleep
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import os

from selenium.webdriver.common.by import By

from_location ='CPH'
to_location = 'LCA'
departure_date =""
arrival_date = ""
sort = ""

URL = 'https://www.kayak.co.uk/flights/{from_location}-{to_location}/2023-09-12/2023-09-30?sort=bestflight_a'.format(to_location=to_location, from_location=from_location)
page_render_wait = 5



driver = webdriver.Chrome()  # or whichever driver you're using
driver.get(URL)
sleep(page_render_wait) # we let the page load to get the popup window

popup_window = '//*[@id="portal-container"]/div/div[2]/div/div/div[2]/div/div[2]/button'
driver.find_element(By.XPATH, popup_window).click()

flight_rows = driver.find_elements(By.CLASS_NAME, 'nrc6-inner')
# print(flight_rows)


# flight_best = driver.find_elements(By.XPATH,'/html/body/div[2]/div[1]/main/div/div[2]/div[2]/div[1]/div[2]/div[1]/div[2]/div[5]/div[2]/div/div/div[1]/div/div[2]/div')
# flight_cheapest = driver.find_elements(By.XPATH,'/html/body/div[2]/div[1]/main/div/div[2]/div[2]/div[1]/div[2]/div[1]/div[2]/div[5]/div[2]/div/div/div[3]/div[2]/div/div/div[1]')
# print(flight_best)
# print(flight_cheapest)

list_of_prices = []
# list_of_companies = []

for WebElement in flight_rows:
    elementHTML = WebElement.get_attribute('outerHTML')
    elementSoup = BeautifulSoup(elementHTML, 'html.parser')
    # print(elementSoup)

    #prices
    price = elementSoup.find(class_ = "f8F1-price-text")
    print(price.text)
    list_of_prices.append(price.text)


print(list_of_prices) 
sleep(50)

