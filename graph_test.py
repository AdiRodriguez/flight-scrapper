import matplotlib.pyplot as plt

# JSON data with "not available" price
data = [
    {'date': 'Wed, 25 Oct', 'price': 761},
    {'date': 'Thu, 26 Oct', 'price': 787},
    {'date': 'Fri, 27 Oct', 'price': 853},
    {'date': 'Sat, 28 Oct', 'price': 677},
    {'date': 'Sun, 29 Oct', 'price': 688},
    {'date': 'Mon, 30 Oct', 'price': 'not available'},
    {'date': 'Tue, 31 Oct', 'price': 811}
]

# Extract dates and prices from JSON, ignoring "not available" prices
dates = []
prices = []

for entry in data:
    if entry['price'] != 'not available':
        dates.append(entry['date'])
        prices.append(entry['price'])

# Create a prettier line graph with yellow color
plt.figure(figsize=(10, 6))
plt.plot(dates, prices, marker='o', linestyle='-', color='yellow', linewidth=2, markersize=8, markeredgecolor='black')
plt.title('Flight Prices Over Time', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Price', fontsize=12)
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)

# Customize the background color
ax = plt.gca()
ax.set_facecolor('#f5f5f5')

# Show the graph
plt.tight_layout()
plt.show()
