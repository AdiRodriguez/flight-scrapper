from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from time import sleep
import re
import pandas as pd

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import pandas as pd
import smtplib
from email.mime.text import MIMEText

# --------------------------------------------------------
# Web Navigation Functions
# --------------------------------------------------------
# NOTE: Web Navigation NEED to be in a "Try and Except" block to avoid runtime ERROR
def close_popup_window():
    popup_window = "RxNS-button-content"
    try:
        driver.find_element(By.CLASS_NAME, popup_window).click()
        print("Clicked cookies pop-up. Sleeping... (2 seconds)")
        sleep(2)
    except:
        ERROR("close_popup_window",popup_window,"pass")


def load_more():
    more_results = "ULvh"
    try:
        driver.find_element(By.CLASS_NAME, more_results).click()
        print("Loading more cards")
        print('Sleeping..... (3 seconds)')
        sleep(3)
    except:
        ERROR("load_more",more_results,"pass")

# --------------------------------------------------------
# Data Scraping Functions
# --------------------------------------------------------
def get_flight_cards():
    HTML_flight_cards = []
    flight_cards_class = "nrc6-inner"
    try:
        flight_rows = driver.find_elements(By.CLASS_NAME, flight_cards_class)
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
        ERROR("get_flight_cards",flight_cards_class,"exit")

def find_best_card(cards):
    html_class = "btf6-badge-wrap"
    best_card = []

    for card in cards:
        try:
            best = card.find(class_= html_class)
            print(best.text)
            best_card.append(card)
        except:
            pass
    return best_card

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
# --------------------------------------------------------
# Miscellaneous Functions
# --------------------------------------------------------
def ERROR(function_name, class_name, exit_or_pass):
    print(f"Reached the except in !!!!{function_name}!!! function...")
    print(f"No Element by the class name: {class_name}")
    if exit_or_pass == "pass":
        print("Skipping...")
    elif exit_or_pass == "exit":
        print("Shuting down...")
        raise SystemExit

def send_email(price, target_price):
    sender_email = 'ady.rodriguez123321@gmail.com'
    receiver_email = 'ady.rodriguez123321@gmail.com'  
    smtp_server = 'smtp.gmail.com'  #SMTP server
    smtp_username = 'ady.rodriguez123321@gmail.com'  
    smtp_password = 'mlcy spbs tydy opxx'  #SMTP password
    message = f"The flight price is below ${target_price}: {price}\n\n go to:{URL} to quickly buy it!"
    msg = MIMEText(message)
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Flight Price Alert"

    try:
        server = smtplib.SMTP(smtp_server)
        server.starttls() # secures our email by encyrpting it
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print(f"Email notification sent for price: {price}")
    except Exception as e:
        print(f"Error sending email: {e}")





if __name__ == '__main__':
    while True:

        URL = "https://www.kayak.co.uk/flights/TYO-LON/2023-10-28-flexible/2023-11-25-flexible?sort=bestflight_a"

        timeout = 100

        browser_driver = Service('/usr/lib/chromium-browser/chromedriver')
        chrome_options = webdriver.ChromeOptions()
        chrome_options.page_load_strategy = 'eager'
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(service=browser_driver,options=chrome_options)
        driver.get(URL)
        sleep(20)
        close_popup_window()
        load_more()
        load_more()
        try:
            WebDriverWait(driver, timeout).until_not(
                EC.text_to_be_present_in_element(
                    (By.CLASS_NAME, "biRz-loading"), "Loading...")
            )
            print("Page loaded successfully!")
            sleep(1) # just in case
            flight_cards = get_flight_cards()

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

            prices = flights_df['Prices']
            loswest_price = min(prices)
            if loswest_price < 500:
                send_email(loswest_price, "500")
                    
        except TimeoutException:
            print("Timed out... Page failed to load properly  ")
        driver.quit()

        sleep((5 * 60 * 60))