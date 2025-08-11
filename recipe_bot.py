import requests
import csv
from datetime import datetime
import os
from requests_oauthlib import OAuth1Session
import pytz

def get_x_session():
    return OAuth1Session(
        os.environ['X_API_KEY'],
        client_secret=os.environ['X_API_SECRET'],
        resource_owner_key=os.environ['X_ACCESS_TOKEN'],
        resource_owner_secret=os.environ['X_ACCESS_TOKEN_SECRET']
    )

def get_crypto_prices():
    """Fetch current BTC and ETH prices from CoinGecko"""
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {
                'btc': data['bitcoin']['usd'],
                'eth': data['ethereum']['usd']
            }
        print(f"Error fetching prices: {response.status_code}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def format_crypto_tweet(prices):
    """Format the crypto prices into a tweet"""
    # Get current time in ET
    et_tz = pytz.timezone('US/Eastern')
    current_time = datetime.now(et_tz)
    time_str = current_time.strftime("%I:%M %p ET")
    
    # Format with emojis and proper formatting
    tweet_text = f"""Crypto Price Update 🚨

BTC: ${prices['btc']:,.0f} USD
ETH: ${prices['eth']:,.0f} USD

{time_str} • {current_time.strftime('%b %d, %Y')}"""
    
    return tweet_text

def post_to_x(tweet_text):
    """Post tweet to X/Twitter"""
    try:
        x_session = get_x_session()
        
        payload = {"text": tweet_text}
        
        print("Posting tweet...")
        response = x_session.post(
            "https://api.twitter.com/2/tweets",
            json=payload
        )
        
        print(f"Response status: {response.status_code}")
        print(f"Response: {response.text}")
        
        return response.status_code == 201
        
    except Exception as e:
        print(f"Error posting to X: {e}")
        return False

def save_to_csv(prices, posted=False):
    """Save record of the post"""
    file_exists = os.path.exists('crypto_posts.csv')
    
    with open('crypto_posts.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Date', 'Time', 'BTC_Price', 'ETH_Price', 'Posted'])
        
        now = datetime.now()
        writer.writerow([
            now.strftime('%Y-%m-%d'),
            now.strftime('%H:%M:%S'),
            prices['btc'],
            prices['eth'],
            'Yes' if posted else 'No'
        ])

def main():
    print(f"Starting crypto price bot at {datetime.now()}")
    
    # Get crypto prices
    prices = get_crypto_prices()
    if not prices:
        print("Failed to get crypto prices")
        return
    
    # Format tweet
    tweet_text = format_crypto_tweet(prices)
    print(f"\nTweet to post:\n{tweet_text}\n")
    
    # Post to X
    posted = post_to_x(tweet_text)
    
    # Save record
    save_to_csv(prices, posted)
    
    if posted:
        print("Successfully posted crypto prices!")
    else:
        print("Failed to post")

if __name__ == "__main__":
    main()
