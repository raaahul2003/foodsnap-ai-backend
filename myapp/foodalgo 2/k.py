import requests

API_KEY = "8MG/uq5sGiV3o2XzbtRqzQ==lLXAvDu3v103aL9X"
food = "paneer"

import requests

api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
query = 'aloo paratha'
response = requests.get(api_url + query, headers={'X-Api-Key': API_KEY})
if response.status_code == requests.codes.ok:
    print(response.text)
else:
    print("Error:", response.status_code, response.text)