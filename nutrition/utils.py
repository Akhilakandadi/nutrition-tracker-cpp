import requests
from django.conf import settings

def get_nutrition(food_name):
    API_KEY = settings.USDA_API_KEY
    BASE_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"

    params = {"query": food_name, "api_key": API_KEY}
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        if data["foods"]:
            food = data["foods"][0]  # Get first result
            #print(food)  # Debugging: print entire food response to see the structure

            # Collect all nutrients from the API response
            nutrients = {nutrient["nutrientName"]: nutrient["value"] for nutrient in food["foodNutrients"]}

            # Now return nutrients including protein, carbs, fats
            return {
                "name": food["description"],
                "calories": nutrients.get("Energy", 0),
                "protein": nutrients.get("Protein", 0),
                "carbs": nutrients.get("Carbohydrate, by difference", 0),
                "fats": nutrients.get("Total lipid (fat)", 0),
                "sugar": nutrients.get("Sugars, total", 0),
                "fiber": nutrients.get("Fiber, total dietary", 0)
            }

    return None
