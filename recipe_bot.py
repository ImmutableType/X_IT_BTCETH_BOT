import requests
import csv
from datetime import datetime
import os

WEBHOOK_URL = "https://maker.ifttt.com/trigger/post_recipe/with/key/okFtDJyKz74JWbigcGtoDM0z25ac8EjrplKmuJQ1iep"

def get_recipes(number=1):  # Changed to 1 recipe for posting
    recipes = []
    for _ in range(number):
        response = requests.get('https://www.themealdb.com/api/json/v1/1/random.php')
        recipes.append(response.json()['meals'][0])
    return recipes

def post_to_ifttt(recipe):
    payload = {
        "value1": datetime.now().strftime('%Y-%m-%d'),
        "value2": f"🍳 Today's Recipe: {recipe['strMeal']}\n\n{recipe['strInstructions'][:150]}...",
        "value3": recipe['strMealThumb']
    }
    requests.post(WEBHOOK_URL, json=payload)

def main():
    recipes = get_recipes()
    for recipe in recipes:
        post_to_ifttt(recipe)

if __name__ == "__main__":
    main()