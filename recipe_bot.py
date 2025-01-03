import requests
import csv
from datetime import datetime

def get_recipes(number=7):  # Week's worth
   recipes = []
   for _ in range(number):
       response = requests.get('https://www.themealdb.com/api/json/v1/1/random.php')
       recipes.append(response.json()['meals'][0])
   return recipes

def save_to_csv(recipes):
   with open('recipes.csv', 'w', newline='') as file:
       writer = csv.writer(file)
       writer.writerow(['Date', 'Title', 'Instructions', 'Image'])
       for recipe in recipes:
           writer.writerow([
               datetime.now().strftime('%Y-%m-%d'),
               recipe['strMeal'],
               recipe['strInstructions'][:200],
               recipe['strMealThumb']
           ])

def main():
   recipes = get_recipes()
   save_to_csv(recipes)

if __name__ == "__main__":
   main()