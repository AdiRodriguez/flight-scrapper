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


def ERROR(function_name, class_name, exit_or_pass):
    print(f"Reached the except in !!!!{function_name}!!! function...")
    print(f"No Element by the class name: {class_name}")
    if exit_or_pass == "pass":
        print("Skipping...")
    elif exit_or_pass == "exit":
        print("Shuting down...")
        raise SystemExit
    
def close_popup_window(driver):
    popup_window = "RxNS-button-content"
    try:
        driver.find_element(By.CLASS_NAME, popup_window).click()
        print("Clicked cookies pop-up. Sleeping... (2 seconds)")
        sleep(2)
    except:
        ERROR("close_popup_window",popup_window,"pass")


def load_more(driver):
    more_results = "ULvh"
    try:
        driver.find_element(By.CLASS_NAME, more_results).click()
        print("Loading more cards")
        print('Sleeping..... (3 seconds)')
        sleep(3)
    except:
        ERROR("load_more",more_results,"pass")
