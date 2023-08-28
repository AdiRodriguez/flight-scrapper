
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
    popup_window = "RxNS-button-content"
    try:
        driver.find_element(By.CLASS_NAME, popup_window).click()
        print("Clicked cookies pop-up. Sleeping... (2 seconds)")
        sleep(2)
    except:
        print("Reached the except in CLOSE_POPUP_WINDOW function...")
        print("Skipping...")
        pass


def load_more():
    more_results = "ULvh" 
    try:
        driver.find_element(By.CLASS_NAME, more_results).click()
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
    
def get_flex_table():
    HTML_flex_table = []
    try:
        WebElements = driver.find_elements(By.CLASS_NAME, 'jPY1')
        for WebElement in WebElements:
            elementHTML = WebElement.get_attribute('outerHTML')
            elementSoup = BeautifulSoup(elementHTML, 'html.parser')
            HTML_flex_table.append(elementSoup)
        if HTML_flex_table == []:
            print("Couldn't find any flights(Array is empty)")
            raise SystemExit
        else:
            return HTML_flex_table
    except:
        print("Couldn't find flight cards to scrape by given class name (check class name again)")
        raise SystemExit

def scrape_prices(cards):
    prices = []
    price_pattern = r'[\d,.]+'
    try:
        for card in cards:
            html_class = "f8F1-price-text"
            price = card.find(class_= html_class)
            price_matches = re.findall(price_pattern, price.text)
            if price_matches:
                numeric_string = price_matches[0]  # Take the first match
                final_price = int(numeric_string.replace(',', ''))  # Remove commas and convert to integer
                prices.append(final_price)
            else:
                print("couldn't find price")
                prices.append("Error")
        return prices
    except:
        print(f"Price class invalid (Can't find class named ---> {html_class}")

def scrape_flight_companies(cards):
    flight_company_a = []
    flight_company_b = []

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
        
    return flight_company_a, flight_company_b

def scrape_flight_schedule(cards):
    time_pattern = r'(\d{2}:\d{2}–\d{2}:\d{2})'
    flight_schedule_a = []
    flight_schedule_b = []

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
    return flight_schedule_a, flight_schedule_b

def scrape_connections(cards):
    flight_connections_a = []
    flight_connections_b = []

    for card in cards:
        connections = card.find_all(class_="JWEO-stops-text")
        for index, connection in enumerate(connections):
            if index == 0:
                flight_connections_a.append(connection.text)
            else:
                flight_connections_b.append(connection.text)
    return flight_connections_a, flight_connections_b

def scrape_estimated_time(cards):
    flight_estimated_time_a = []
    flight_estimated_time_b = []

    for card in cards:
        times = card.find_all(class_="xdW8 xdW8-mod-full-airport")
        for index, time in enumerate(times):
            if index == 0:
                flight_estimated_time_a.append(time.text)
            else:
                flight_estimated_time_b.append(time.text)
    return flight_estimated_time_a, flight_estimated_time_b

# def get_stops(cards):
#     for card in cards:
#         test = card.find(class_="EFvI-ap-info")
#         print(test.text)

def scrape_flex_table(cards):
    prices = []
    price_pattern = r'[\d,.]+'
    for i in range(21,28):
        price_matches = re.findall(price_pattern, cards[i].text)
        if price_matches:
            numeric_string = price_matches[0]  # Take the first match
            final_price = int(numeric_string.replace(',', ''))  # Remove commas and convert to integer
            prices.append(final_price)
        else:
            print("couldn't find price")
    return prices

# NOTE: Do the rest of the "get" functions (If needed)

# --------------------------------------------------------
# Dummy Data
# --------------------------------------------------------
from_location = 'LIS'
to_location = 'MEX'
date_start = "2023-09-28-flexible"
date_end = "2023-09-29-flexible"
# NOTE: Move "...-flexible" to the URL

URL = 'https://www.kayak.co.uk/flights/{from_location}-{to_location}/{date_start}/{date_end}?sort=bestflight_a'.format(
    to_location=to_location, from_location=from_location, date_start=date_start, date_end=date_end)

# --------------------------------------------------------
# Main Code
# --------------------------------------------------------
if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get(URL)
    sleep(30)  
    close_popup_window()
    load_more()
    load_more()
    flight_cards = get_flight_cards()
    flight_cards_flex = get_flex_table()

    flight_prices = scrape_prices(flight_cards)
    schedule_a, schedule_b = scrape_flight_schedule(flight_cards)
    company_a, company_b = scrape_flight_companies(flight_cards)
    connections_a, connections_b = scrape_connections(flight_cards)
    time_a, time_b = scrape_estimated_time(flight_cards)

    flex_prices_3 = scrape_flex_table(flight_cards_flex)
    print(flex_prices_3)

    flights_df = pd.DataFrame({'Prices': flight_prices,
                           'Outbound Schedule': schedule_a,
                           'Outbound Estimated Time': time_a,
                           'Outbound Company': company_a,
                           'Outbound Connections': connections_a,
                           'Inbound Schedule': schedule_b,
                           'Inbound Estimated Time': time_b,
                           'Inbound Company': company_b,
                           'Inbound Connections': connections_b 
                           })
    print(flights_df)

    sleep(25)


#NOTE:  Test -  driver.save_screenshot('./screenshots/pythonscraping.png') 

#TODO: Take care of edge cases in scrape_flex_table(cards) - ex: if price before given date is blank