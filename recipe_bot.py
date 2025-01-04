import requests
import csv
from datetime import datetime
import os
from requests_oauthlib import OAuth1Session

def get_x_session():
    return OAuth1Session(
        os.environ['X_API_KEY'],
        client_secret=os.environ['X_API_SECRET'],
        resource_owner_key=os.environ['X_ACCESS_TOKEN'],
        resource_owner_secret=os.environ['X_ACCESS_TOKEN_SECRET']
    )

def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    return None

def upload_media_to_x(image_data):
    x_session = get_x_session()
    response = x_session.post(
        "https://upload.twitter.com/1.1/media/upload.json",
        files={"media": image_data}
    )
    if response.status_code == 200:
        return response.json()['media_id_string']
    return None

def get_recipes(number=1):
    recipes = []
    for _ in range(number):
        response = requests.get('https://www.themealdb.com/api/json/v1/1/random.php')
        recipes.append(response.json()['meals'][0])
    return recipes

def format_ingredients_and_instructions(recipe):
    # Gather all ingredients and their measurements
    ingredients_list = []
    for i in range(1, 21):  # MealDB provides up to 20 ingredients
        ingredient = recipe.get(f'strIngredient{i}')
        measure = recipe.get(f'strMeasure{i}')
        if ingredient and ingredient.strip() and measure and measure.strip():
            ingredients_list.append(f"• {measure} {ingredient}")
    
    # Join ingredients with newlines
    ingredients_section = "\n".join(ingredients_list)
    
    # Format instructions
    instructions = recipe['strInstructions'].replace('. ', '.\n\n')
    
    # Combine both sections
    return f"🧂 Ingredients:\n\n{ingredients_section}\n\n📝 Method:\n\n{instructions}"

def post_to_x(recipe):
    # Define emojis as variables
    cooking = "🍳"
    sparkle = "✨"
    plate = "🍽"

    # Pre-format instructions
    formatted_content = format_ingredients_and_instructions(recipe)

    # Build tweet text piece by piece
    tweet_parts = [
        f"{cooking} Today's Recipe: {recipe['strMeal']} {sparkle}",
        "",
        formatted_content,
        "",
        f"{sparkle} Enjoy your homemade {recipe['strMeal']}! {plate}"
    ]

    # Join all parts with newlines
    tweet_text = '\n'.join(tweet_parts)

    # Debug print
    print(f"Preparing tweet with {len(tweet_text)} characters")
    
    try:
        x_session = get_x_session()
        
        # Handle image upload
        print("Downloading image...")
        image_data = download_image(recipe['strMealThumb'])
        
        payload = {"text": tweet_text}
        
        if image_data:
            print("Uploading image to X...")
            media_id = upload_media_to_x(image_data)
            if media_id:
                payload["media"] = {"media_ids": [media_id]}
        
        print("Posting tweet...")
        response = x_session.post(
            "https://api.twitter.com/2/tweets",
            json=payload
        )
        
        # Debug print
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.text}")
        
        return response.status_code == 201
        
    except Exception as e:
        print(f"Error posting to X: {e}")
        return False

def save_to_csv(recipe, posted=False):
    file_exists = os.path.exists('recipes.csv')
    
    with open('recipes.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Date', 'Title', 'Full Instructions', 'Image URL', 'Posted'])
        
        writer.writerow([
            datetime.now().strftime('%Y-%m-%d'),
            recipe['strMeal'],
            recipe['strInstructions'],
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