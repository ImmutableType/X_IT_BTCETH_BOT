import requests
import csv
from datetime import datetime
import os

WEBHOOK_URL = "https://maker.ifttt.com/trigger/post_recipe/with/key/okFtDJyKz74JWbigcGtoDM0z25ac8EjrplKmuJQ1iep"

def get_recipes(number=1):
    recipes = []
    for _ in range(number):
        response = requests.get('https://www.themealdb.com/api/json/v1/1/random.php')
        recipes.append(response.json()['meals'][0])
    return recipes

def post_to_ifttt(recipe):
    tweet_text = (f"🍳 Today's Recipe: {recipe['strMeal']}\n\n"
                 f"Instructions:\n{recipe['strInstructions']}")
    
    payload = {
        "value1": datetime.now().strftime('%Y-%m-%d'),
        "value2": tweet_text,
        "value3": recipe['strMealThumb']
    }
    response = requests.post(WEBHOOK_URL, json=payload)
    return response.status_code == 200

def save_to_csv(recipe, posted=False):
    file_exists = os.path.exists('recipes.csv')
    
    with open('recipes.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Date', 'Title', 'Full Instructions', 'Image URL', 'Posted'])
        
        # Store complete recipe in CSV
        writer.writerow([
            datetime.now().strftime('%Y-%m-%d'),
            recipe['strMeal'],
            recipe['strInstructions'],  # Full instructions
            recipe['strMealThumb'],
            'Yes' if posted else 'No'
        ])

def main():
    recipes = get_recipes()
    for recipe in recipes:
        posted = post_to_ifttt(recipe)
        save_to_csv(recipe, posted)

if __name__ == "__main__":
    main()