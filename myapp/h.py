import requests

def get_nutrition_from_food(food_name):
    """
    Fetches nutrition information for a given food name using Open Food Facts API.
    """
    try:
        if not isinstance(food_name, str) or not food_name.strip():
            raise ValueError("Food name must be a non-empty string.")

        # API endpoint for searching products
        url = "https://world.openfoodfacts.org/cgi/search.pl"
        params = {
            "search_terms": food_name,
            "search_simple": 1,
            "action": "process",
            "json": 1,
            "page_size": 1  # Get only the first matching product
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get("products"):
            return f"No nutrition data found for '{food_name}'."

        product = data["products"][0]
        product_name = product.get("product_name", "Unknown Product")
        nutriments = product.get("nutriments", {})

        # Extract nutrition name and value
        nutrition_info = {}
        for key, value in nutriments.items():
            if isinstance(value, (int, float, str)):
                nutrition_info[key] = value

        return {
            "product_name": product_name,
            "nutrition": nutrition_info
        }

    except requests.exceptions.RequestException as e:
        return f"Network error: {e}"
    except ValueError as ve:
        return str(ve)
    except Exception as e:
        return f"An error occurred: {e}"


# Example usage
if __name__ == "__main__":
    food = "banana"
    result = get_nutrition_from_food(food)
    print(result)