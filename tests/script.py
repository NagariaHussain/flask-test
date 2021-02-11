# ----------------------------------
# ONLY RUN WHEN FLASK APP IS RUNNING
# ----------------------------------

# To make HTTP requests
import requests

# Local host url, port 5000
URL = "http://127.0.0.1:5000"

# Products to create
products = [
    'Apple iPhone 12',
    'HP Envy 13',
    'Samsung Galaxy S21',
    'Apple Watch Series 3'
]

# Locations to create
locations = [
    'Mumbai',
    'Paris',
    'Hyderabad',
    'Las Vegas'
]

# Create products
for product in products:
    requests.post(f"{URL}/product/add", {"product_id": product})

# Create locations
for location in locations:
    requests.post(f"{URL}/location/add", {"location_id": location})

# To add initial stocks
# Movements to make
movements = [
    {
        "product_id": "Apple iPhone 12",
        "to_location": "Mumbai",
        "qty": "100"
    },
    {
        "product_id": "Samsung Galaxy S21",
        "to_location": "Paris",
        "qty": "300"
    },
    {
        "product_id": "Apple iPhone 12",
        "to_location": "Hyderabad",
        "qty": "400"
    },
    {
        "product_id": "Apple Watch Series 3",
        "to_location": "Las Vegas",
        "qty": "500"
    },
    {
        "product_id": "HP Envy 13",
        "to_location": "Mumbai",
        "qty": "1000"
    }
]

for pm in movements:
    requests.get(f"{URL}/movement/move", pm)



