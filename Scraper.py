
from time import sleep
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import os

from selenium.webdriver.common.by import By

import re

# Web Navigation Functions
# --------------------------------------------------------
def close_popup_window():
    popup_window = '//*[@id="portal-container"]/div/div[2]/div/div/div[2]/div/div[2]/button'
    try:
        driver.find_element(By.XPATH, popup_window).click()
        print("Clicked cookies pop-up. Sleeping... (2 seconds)")
        sleep(2)
    except:
        print("Reached the except in CLOSE_POPUP_WINDOW function...")
        print("Skipping...")
        pass


def load_more():
    more_results = "/html/body/div[2]/div[1]/main/div/div[2]/div[2]/div[1]/div[2]/div[1]/div[3]/div[1]/div/div/div"   # Full Xpath
    try:
        driver.find_element(By.XPATH, more_results).click()
        print("Loading more cards")
        print('Sleeping..... (3 seconds)')
        sleep(3)
    except:
        print("Reached the except in LOAD_MORE function...")
        pass

# --------------------------------------------------------
# Data Scraping Functions
# --------------------------------------------------------

def get_flight_cards():
    HTML_flight_cards = []
    try:
        flight_rows = driver.find_elements(By.CLASS_NAME, 'nrc6-inner')
        for WebElement in flight_rows:
            elementHTML = WebElement.get_attribute('outerHTML')
            elementSoup = BeautifulSoup(elementHTML, 'html.parser')
            HTML_flight_cards.append(elementSoup)
        if len(HTML_flight_cards) == 0:
            print("Couldn't find any flights (array is empty)")
            raise SystemExit
        else:
            return HTML_flight_cards
    except:
        print("Couldn't find flight cards to scrape by given class name (check class name again)")
        raise SystemExit


def get_prices(cards):
    price_pattern = r'[\d,.]+'
    for card in cards:
        price = card.find(class_="f8F1-price-text")
        price_matches = re.findall(price_pattern, price.text)
        if price_matches:
            numeric_string = price_matches[0]  # Take the first match
            final_price = int(numeric_string.replace(',', ''))  # Remove commas and convert to integer
            flight_prices.append(final_price)
        else:
            print("couldn't find price")



def get_flight_companies(cards):
    for card in cards:
        companies = card.find(class_="J0g6-operator-text")
        company_list = companies.text.split(",")
        outbound_flight_company = company_list[0]
        flight_company_a.append(outbound_flight_company)
        if len(company_list) > 1:
            inbound_flight_company = company_list[1]
            flight_company_b.append(inbound_flight_company)
        else:
            inbound_flight_company = company_list[0]
            flight_company_b.append(inbound_flight_company)



def get_flight_schedule(cards):
    time_pattern = r'(\d{2}:\d{2}–\d{2}:\d{2})'
    for card in cards:
        flights_time = card.find_all(class_="VY2U")
        for index, flight_time in enumerate(flights_time):
            time_pattern_search = re.search(time_pattern, flight_time.text)
            final_time_string = time_pattern_search.group()

            if final_time_string:
                if index == 0:
                    flight_schedule_a.append(final_time_string)
                else:
                    flight_schedule_b.append(final_time_string)


def get_stops(cards):
    for card in cards:
        test = card.find(class_="EFvI-ap-info")
        print(test.text)


def get_connections(cards):

    for card in cards:
        connections = card.find_all(class_="JWEO-stops-text")
        for index, connection in enumerate(connections):
            if index == 0:
                flight_connections_a.append(connection.text)
            else:
                flight_connections_b.append(connection.text)


def get_estimated_time(cards):

    for card in cards:
        times = card.find_all(class_="xdW8 xdW8-mod-full-airport")
        for index, time in enumerate(times):
            if index == 0:
                flight_estimated_time_a.append(time.text)
            else:
                flight_estimated_time_b.append(time.text)

# NOTE: Do the rest of the "get" functions (If needed)

# --------------------------------------------------------
# Dummy Data
# --------------------------------------------------------
from_location = 'LIS'
to_location = 'NYC'
date_start = "2023-08-29-flexible"
date_end = "2023-09-15-flexible"
# NOTE: Move "...-flexible" to the URL

URL = 'https://www.kayak.co.uk/flights/{from_location}-{to_location}/{date_start}/{date_end}?sort=bestflight_a'.format(
    to_location=to_location, from_location=from_location, date_start=date_start, date_end=date_end)



# --------------------------------------------------------
# Flight Cards Data
# --------------------------------------------------------
flight_prices = []

flight_company_a = []
flight_company_b = []

flight_schedule_a = []
flight_schedule_b = []

flight_connections_a = []
flight_connections_b = []

flight_estimated_time_a = []
flight_estimated_time_b = []
# --------------------------------------------------------
# Main Code
# --------------------------------------------------------
if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get(URL)
    sleep(20)  
    close_popup_window()
    load_more()
    load_more()
    cards = get_flight_cards()
    get_prices(cards)
    get_flight_schedule(cards)
    get_estimated_time(cards)
    get_flight_companies(cards)
    get_connections(cards)

    flights_df = pd.DataFrame({'Prices': flight_prices,
                           'Outbound Schedule': flight_schedule_a,
                           'Outbound Estimated Time': flight_estimated_time_a,
                           'Outbound Company': flight_company_a,
                           'Outbound Connections': flight_connections_a,
                           'Inbound Schedule': flight_schedule_b,
                           'Inbound Estimated Time': flight_estimated_time_b,
                           'Inbound Company': flight_company_b,
                           'Inbound Connections': flight_connections_b 
                           })

    print(flights_df)

    driver.save_screenshot('./screenshots/pythonscraping.png') # NOTE: Testing

    sleep(25)


# TODO: Add User input
# TODO: Adjust sleep time accordingly - Sometimes, the page will load incorrect data (usually the first load of the day) and will needs more time to fully load the up-to-date flights
# TODO: Do I need to add "Try and except" in each scraping function? - Ask Achmed for "wisdom"
# TODO: Nest all scraping functions in a single FUNction (not fun)
# TODO: Send the data to Email
# TODO: DO SOMETHING WITH THE "BEST" AND "CHEAPEST" FLIGHT CARDS (plus, remove first "ad" flight card)
# TODO: Add currency converter 

# Few comments:
# - Why are functions called: "get_" when they don't return anything
# - Together with #1: global state bad, return results from functions instead of altering global variables
# - "Sleep" is always a disaster waiting to happen, check if you can use events like "OnDocumentReady" or whatever it's called in the Chrome webdriver
# - "/html/body/div[2]/div[1]/main/div/div[2]/div[2]/div[1]/div[2]/div[1]/div[3]/div[1]/div/div/div"  -> the fuck, use class names or ids to find an element 


# NOTE: For Achmed - When Selenium/BeautifulSoup can't find the given element/HTML (for example: flight_rows = driver.find_elements(By.CLASS_NAME, 'nrc6-inner')), The script crashes and closes itself
