# USDA FoodData Central (Government Open API)
# Completely free and unlimited
# Requires registration for an API key
# Data source: U.S. Department of Agriculture
# Returns detailed nutrients for thousands of foods
# Sign up: https://fdc.nal.usda.gov/api-key-signup.html


import requests
api_key = "wHgCIYjR9w2Y0hoeu2eGplf4n8WM1XWSC3jQdhcv"
food = "rice pathiri"
url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={food}&api_key={api_key}"

response = requests.get(url)
data = response.json()
print(data["foods"][0]["description"])
print(data["foods"][0]["foodNutrients"])
