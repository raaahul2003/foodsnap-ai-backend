import google.generativeai as genai
import json

# Configure API Key
genai.configure(api_key="YOUR_GEMINI_API_KEY")

def get_food_details(food_name):
    try:
        model = genai.GenerativeModel("gemini-latest-flash")

        prompt = f"""
        You are a nutrition expert.

        Given the food name: {food_name}

        Return:
        1. List of main ingredients
        2. Approximate nutrition values per 100g:
           - Calories (kcal)
           - Protein (g)
           - Carbohydrates (g)
           - Fat (g)
           - Sugar (g)
           - Fiber (g)

        Return ONLY valid JSON in this format:

        {{
            "food_name": "",
            "ingredients": [],
            "nutrition_per_100g": {{
                "calories": "",
                "protein": "",
                "carbohydrates": "",
                "fat": "",
                "sugar": "",
                "fiber": ""
            }}
        }}
        """

        response = model.generate_content(prompt)

        if not response.text:
            return None

        # Clean JSON output
        cleaned = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(cleaned)

    except Exception as e:
        print("Gemini Error:", e)
        return None


# Example
result = get_food_details("Chicken Biryani")
print(json.dumps(result, indent=4))