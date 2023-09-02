
from time import sleep
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import re

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from datetime import datetime


import matplotlib.pyplot as plt


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
    
#NOTE: FIX!! 
def scrape_flex_table_dates():
    HTML_flex_table = []
    try:
        WebElements = driver.find_elements(By.CLASS_NAME, 'VuLg')
        for WebElement in WebElements:
            elementHTML = WebElement.get_attribute('outerHTML')
            elementSoup = BeautifulSoup(elementHTML, 'html.parser')
            HTML_flex_table.append(elementSoup.text)
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
            price = card.find(class_=html_class)
            price_matches = re.findall(price_pattern, price.text)
            if price_matches:
                numeric_string = price_matches[0]  # Take the first match
                # Remove commas and convert to integer
                final_price = int(numeric_string.replace(',', ''))
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

def scrape_flex_table_prices_3(cards):
    prices = []
    price_pattern = r'[\d,.]+'
    for i in range(21, 28):
        price_matches = re.findall(price_pattern, cards[i].text)
        if price_matches:
            numeric_string = price_matches[0]  # Take the first match
            # Remove commas and convert to integer
            final_price = int(numeric_string.replace(',', ''))
            prices.append(final_price)
        else:
            print("Couldn't find price")
            prices.append("Not Available ")
    return prices

#NOTE: FIX!!
def scrape_flex_table_dates_3(list):
    new_list = list[:7]
    return new_list

# NOTE: Do the rest of the "get" functions (If needed)

def change_date_format(date):
    date_object = datetime.strptime(date, "%Y-%m-%d")
    formatted_date = date_object.strftime("%a, %d %b")
    return (formatted_date)



def create_flight_data_json(dates, prices):
    if len(dates) != len(prices):
        raise ValueError("Dates and prices lists must have the same length")

    flight_data = []

    for date, price in zip(dates, prices):
        flight_data.append({"date": date, "price": price})
    return flight_data

def create_graph(json):
    dates = []
    prices = []

    for entry in json:
        if entry['price'] != 'not available':
            dates.append(entry['date'])
            prices.append(entry['price'])

    plt.figure(figsize=(10, 6))
    plt.plot(dates, prices, marker='o', linestyle='-', color='yellow', linewidth=2, markersize=8, markeredgecolor='black')
    plt.title('Flight Prices Over Time', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Price', fontsize=12)
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)

    ax = plt.gca()
    ax.set_facecolor('#f5f5f5')

    # Show the graph
    plt.tight_layout()
    plt.show()

# --------------------------------------------------------
# Dummy Data
# --------------------------------------------------------
from_location = 'TYO'
to_location = 'LON'
date_start = "2023-10-28"
date_end = "2023-11-25"


URL = 'https://www.kayak.co.uk/flights/{from_location}-{to_location}/{date_start}-flexible/{date_end}-flexible?sort=bestflight_a'.format(
    to_location=to_location, from_location=from_location, date_start=date_start, date_end=date_end)
timeout = 40

# --------------------------------------------------------
# Main Code
# --------------------------------------------------------
if __name__ == '__main__':
    options = Options()
    options.page_load_strategy = 'eager'
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    sleep(3)
    close_popup_window()
    # load_more()
    # load_more()
    try:
        WebDriverWait(driver, timeout).until_not(
            EC.text_to_be_present_in_element(
                (By.CLASS_NAME, "col-advice"), "Loading...")
        )
        print("Page loaded successfully!")
        sleep(1) # just in case
        flight_cards = get_flight_cards()
        flight_price_cards_flex = get_flex_table()
        flight_date_cards_flex = scrape_flex_table_dates()

        flight_prices = scrape_prices(flight_cards)
        schedule_a, schedule_b = scrape_flight_schedule(flight_cards)
        company_a, company_b = scrape_flight_companies(flight_cards)
        connections_a, connections_b = scrape_connections(flight_cards)
        time_a, time_b = scrape_estimated_time(flight_cards)

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
        # print(flights_df)

        flex_prices_3 = scrape_flex_table_prices_3(flight_price_cards_flex)
        flex_dates_3 = scrape_flex_table_dates_3(flight_date_cards_flex)
        flex_json = create_flight_data_json(flex_dates_3,flex_prices_3)
        # print(flex_prices_3)
        # print(flex_dates_3)
        # print(flex_json)
        create_graph(flex_json)
    except TimeoutException:
        print("Timed out... Page failed to load properly  ")
    
    driver.quit()

# NOTE:  Test -  driver.save_screenshot('./screenshots/pythonscraping.png')
# NOTE: Implicit, Explicit Fluent wait ---> LEARN
# NOTE: VuLg
# TODO: Take care of edge cases in scrape_flex_table(cards) - ex: if price before given date is blank ----> I THINK I FIXED IT


