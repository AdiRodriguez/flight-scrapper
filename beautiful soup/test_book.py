import requests
from bs4 import BeautifulSoup
import re

# # URL of the book product page (צומת ספרים)
# url = 'https://www.booknet.co.il/%D7%9E%D7%95%D7%A6%D7%A8%D7%99%D7%9D/%d7%9e%d7%95%d7%a4%d7%a2-%d7%94%d7%91%d7%95%d7%91%d7%95%d7%aa-62512015583'

# # Send an HTTP GET request to the URL
# response = requests.get(url)

# # Parse the HTML content of the page using Beautiful Soup
# soup = BeautifulSoup(response.content, 'html.parser')

# # Find the wanted elements containing the price and name
# price_element = soup.find('h3', {'id': 'product-page-price'})
# name_element = soup.find('h1', {'id': 'product-page-title'})
# print(name_element.text[::-1])


# if price_element and name_element:
#     book_price = price_element.get_text()
#     numbers_only = (re.findall(r'\d+', book_price))
#     numbers_value = numbers_only[0]
#     print(f"The price of the book is: {book_price}")
# else:
#     print("Price not found on the page")


# URL of the book product page (צומת ספרים)
url = 'https://www.booknet.co.il/%d7%9e%d7%91%d7%a6%d7%a2-%d7%a8%d7%91%d7%99-%d7%9e%d7%9b%d7%a8'

# Send an HTTP GET request to the URL
response = requests.get(url)

# Parse the HTML content of the page using Beautiful Soup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the wanted elements containing the price and name
price_element = soup.find_all('div', {'class': 'price'})
print(price_element)
for price in price_element:
    book_price = re.findall(r'\d+', price.find('ins').text)
    print(book_price[0])
# name_element = soup.find('h1', {'id': 'product-page-title'})
# print(name_element.text[::-1])


# if price_element and name_element:
#     book_price = price_element.get_text()
#     numbers_only = (re.findall(r'\d+', book_price))
#     numbers_value = numbers_only[0]
#     print(f"The price of the book is: {book_price}")
# else:
#     print("Price not found on the page")





