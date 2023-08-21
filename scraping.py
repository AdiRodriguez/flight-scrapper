
from time import sleep
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import os

from selenium.webdriver.common.by import By

import re

from_location ='TLV'
to_location = 'NYC'
departure_date =""
arrival_date = ""
sort = ""

URL = 'https://www.kayak.co.uk/flights/{from_location}-{to_location}/2023-09-12/2023-09-30?sort=bestflight_a'.format(to_location=to_location, from_location=from_location)
page_render_wait = 5


list_of_prices = []

list_going_flight_schedule = []
list_going_flight_connections = []
list_going_flight_airport_code = []

list_returning_flight_schedule = []
list_returning_flight_connections = []
list_returning_flight_airport_code = []

list_of_companies = []
# list_of_flight_schedule_to = []
# list_of_flight_schedule_back = []

## TO-DO
    # NEED TO ADD (Try and Expect) for (Driver.get(URL))
#--------------------------------START--------------------------------
driver = webdriver.Chrome()  # or whichever driver you're using
driver.get(URL)
sleep(page_render_wait) 

popup_window = '//*[@id="portal-container"]/div/div[2]/div/div/div[2]/div/div[2]/button'
driver.find_element(By.XPATH, popup_window).click()

flight_rows = driver.find_elements(By.CLASS_NAME, 'nrc6-inner')
for WebElement in flight_rows:
    elementHTML = WebElement.get_attribute('outerHTML')
    elementSoup = BeautifulSoup(elementHTML, 'html.parser')


    #prices
    price = elementSoup.find(class_ = "f8F1-price-text")
    price_pattern = r'[\d,.]+'
    price_matches = re.findall(price_pattern, price.text)
    if price_matches:    
        numeric_string = price_matches[0]  # Take the first match
        integer_value = int(numeric_string.replace(',', ''))  # Remove commas and convert to integer
        list_of_prices.append(integer_value)
    else:
        print("No numeric value found in the input string.")
    


    #flight companies
    companies = elementSoup.find(class_ = "J0g6-operator-text")
    company_list = companies.text.split(",")
    list_of_companies.append(company_list)


    # time and airports
    flight_time_and_company = elementSoup.find_all(class_ = "VY2U")
    for index, flight_time in enumerate(flight_time_and_company):
            
            #time
            time_pattern = r'(\d{2}:\d{2}–\d{2}:\d{2})'
            time_match = re.search(time_pattern, flight_time.text)
            time_range = time_match.group()

            if time_match:
                            
                if index == 0:
                    list_going_flight_schedule.append(time_range)
                else:
                     list_returning_flight_schedule.append(time_range)
            else:
                 print(f"No time range found for flight {index}.")


            # airports: NEED TO FIXXXXXXXXX
            airport_pattern = r'([A-Z]{3})'
            airport_match = re.search(airport_pattern, flight_time.text)
            airport_codes = airport_match.group()
            print(airport_codes)


    flight_connections = elementSoup.find_all(class_ = "JWEO-stops-text")
    for index, flight_connection in enumerate(flight_connections):
        # print(flight_connection.text)
        if index == 0:
            list_going_flight_connections.append(flight_connection.text)
        else:
            list_returning_flight_connections.append(flight_connection.text)

         


# print(f"prices list: {list_of_prices}")
# print(f"companies list: {list_of_companies}")
# print(f"going flights list: {list_going_flight_schedule}")
# print(f"returning flights list: {list_returning_flight_schedule}")
# print(f"going flights connections: {list_going_flight_connections}")
# print(f"returning flights connections: {list_returning_flight_connections}")

list_of_lists = [list_of_prices, list_of_companies, list_going_flight_schedule, list_returning_flight_schedule, list_going_flight_connections, list_returning_flight_connections]
list_lengths = [len(lst) for lst in list_of_lists]

if all(length == list_lengths[0] for length in list_lengths):
    combined_dict = {}

    for i in range(list_lengths[0]):
        combined_dict[i] = {
            "price" : list_of_prices[i],
            "outbound": {
                "airline": "",
                "departure_airport": "",
                "destination_airport": "",
                "departure_time": "",
                "arrival_time": "",
                "passenger_count": "",

            },
            "return": {
                "airline": "",
                "departure_airport": "",
                "destination_airport": "",
                "departure_time": "",
                "arrival_time": "",
                "passenger_count": "",
            }
        }

    print(combined_dict)
else:
    print("Lists are not of the same length.")

            
sleep(5000)



# flight_details = {
# 	"outbound": {
#     	"airline": "",
#     	"departure_airport": "",
#     	"destination_airport": "",
#     	"departure_time": "",
#     	"arrival_time": "",
#     	"passenger_count": "",

# 	},
# 	"return": {
#     	"airline": "",
#     	"departure_airport": "",
#     	"destination_airport": "",
#     	"departure_time": "",
#     	"arrival_time": "",
#     	"passenger_count": "",
# 	}
# }


# print(f"prices list: {len(list_of_prices)}")
# print(f"companies list: {len(list_of_companies)}")
# print(f"going flights list: {len(list_going_flight_schedule)}")
# print(f"returning flights list: {len(list_returning_flight_schedule)}")
# print(f"going flights connections: {len(list_going_flight_connections)}")
# print(f"returning flights connections: {len(list_returning_flight_connections)}")


def get_price(card):
    price = card.find(class_ = "f8F1-price-text")
    price_pattern = r'[\d,.]+'
    price_matches = re.findall(price_pattern, price.text)
    if price_matches:    
        numeric_string = price_matches[0]  # Take the first match
        integer_value = int(numeric_string.replace(',', ''))  # Remove commas and convert to integer
        list_of_prices.append(integer_value)
    else:
        print("No numeric value found in the input string.")

def get_flight_companies(card):
    companies = card.find(class_ = "J0g6-operator-text")
    company_list = companies.text.split(",")
    list_of_companies.append(company_list)
    
def get_time(card):
    flight_time_and_company = card.find_all(class_ = "VY2U")
    for index, flight_time in enumerate(flight_time_and_company):
            #time
            time_pattern = r'(\d{2}:\d{2}–\d{2}:\d{2})'
            time_match = re.search(time_pattern, flight_time.text)
            time_range = time_match.group()

            if time_match:
                            
                if index == 0:
                    list_going_flight_schedule.append(time_range)
                else:
                    list_returning_flight_schedule.append(time_range)
            else:
                 print(f"No time range found for flight {index}.")
def get_connections(card):
    flight_connections = card.find_all(class_ = "JWEO-stops-text")
    for index, flight_connection in enumerate(flight_connections):
        # print(flight_connection.text)
        if index == 0:
            list_going_flight_connections.append(flight_connection.text)
        else:
            list_returning_flight_connections.append(flight_connection.text)

