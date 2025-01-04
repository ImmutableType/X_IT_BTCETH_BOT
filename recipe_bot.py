import requests
import csv
from datetime import datetime
import os
import tweepy

# Replace IFTTT webhook with X API setup
def get_x_client():
    client = tweepy.Client(
        bearer_token=os.environ['X_BEARER_TOKEN'],
        consumer_key=os.environ['X_API_KEY'],
        consumer_secret=os.environ['X_API_SECRET'],
        access_token=os.environ['X_ACCESS_TOKEN'],
        access_token_secret=os.environ['X_ACCESS_TOKEN_SECRET']
    )
    return client

def get_recipes(number=1):
    recipes = []
    for _ in range(number):
        response = requests.get('https://www.themealdb.com/api/json/v1/1/random.php')
        recipes.append(response.json()['meals'][0])
    return recipes

def post_to_x(recipe):
    # Format tweet text
    tweet_text = f"""🍳 Today's Recipe: {recipe['strMeal']}

Instructions:
{recipe['strInstructions']}"""

    # Debug print
    print(f"Sending tweet with {len(tweet_text)} characters")
    
    try:
        client = get_x_client()
        # Create tweet
        response = client.create_tweet(text=tweet_text)
        
        # Debug print
        print(f"Tweet posted successfully: {response}")
        return True
        
    except Exception as e:
        print(f"Error posting to X: {e}")
        return False

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
        posted = post_to_x(recipe)
        save_to_csv(recipe, posted)

if __name__ == "__main__":
    main()