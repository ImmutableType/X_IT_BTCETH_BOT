import requests
import csv
from datetime import datetime
import os

def get_recipes(number=7):
    recipes = []
    for _ in range(number):
        response = requests.get('https://www.themealdb.com/api/json/v1/1/random.php')
        recipes.append(response.json()['meals'][0])
    return recipes

def format_recipe(recipe):
    return [
        datetime.now().strftime('%Y-%m-%d'),
        recipe['strMeal'],
        f"🍳 Today's Recipe: {recipe['strMeal']}\n\n{recipe['strInstructions'][:150]}...",
        recipe['strMealThumb']
    ]

def save_to_csv(recipes):
    with open('recipes.csv', 'w', newline='\n') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Title', 'Post Content', 'Image URL'])
        for recipe in recipes:
            writer.writerow(format_recipe(recipe))

def main():
    recipes = get_recipes()
    save_to_csv(recipes)

if __name__ == "__main__":
    main()