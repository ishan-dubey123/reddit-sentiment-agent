"""
Reddit Sentiment Analysis Agent
--------------------------------
Continuously monitors a specified subreddit, fetches the latest posts,
analyzes sentiment using keyword matching, and logs results to a JSON file.

Author: Ishan Dubey
For: Binox Limited FDE Technical Assessment (G2 Task)
"""

import requests
import json
import time
from datetime import datetime

# ================= CONFIGURATION =================
# These settings can be changed without modifying the logic
SUBREDDIT = "worldnews"      # Subreddit to monitor (e.g., 'technology', 'python')
POST_LIMIT = 5               # Number of new posts to fetch per cycle
SLEEP_SECONDS = 60           # Wait time between monitoring cycles (seconds)
CYCLES = 3                   # Number of cycles to run (for demo; set to large number for continuous)
# =================================================

# Keyword lists for sentiment analysis
POSITIVE_WORDS = [
    'great', 'good', 'amazing', 'excellent', 'love', 'best', 'awesome',
    'fantastic', 'cool', 'nice', 'perfect', 'wonderful', 'brilliant'
]
NEGATIVE_WORDS = [
    'bad', 'terrible', 'awful', 'worst', 'hate', 'sucks', 'useless',
    'trash', 'garbage', 'annoying', 'stupid', 'disappointing', 'boring'
]

def analyze_sentiment(text):
    """
    Determine sentiment of a given text string using keyword matching.
    
    Args:
        text (str): The input text (e.g., post title).
    
    Returns:
        str: 'positive', 'negative', or 'neutral'
    """
    text_lower = text.lower()
    pos_count = sum(1 for word in POSITIVE_WORDS if word in text_lower)
    neg_count = sum(1 for word in NEGATIVE_WORDS if word in text_lower)
    
    if pos_count > neg_count:
        return "positive"
    elif neg_count > pos_count:
        return "negative"
    else:
        return "neutral"

def fetch_and_analyze():
    """
    Fetch new posts from Reddit's public JSON API, analyze sentiment,
    and return a list of structured post data.
    
    Returns:
        list: List of dictionaries, each containing title, score, sentiment, url, timestamp.
              Returns empty list if request fails.
    """
    # Construct the API URL for the subreddit's new posts
    url = f"https://www.reddit.com/r/{SUBREDDIT}/new.json?limit={POST_LIMIT}"
    
    # A User-Agent header is required to avoid being blocked by Reddit
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"  Network error: {e}")
        return []
    
    if response.status_code != 200:
        print(f"  HTTP error: {response.status_code}")
        return []
    
    data = response.json()
    posts = []
    # Reddit's JSON structure: data -> children -> child -> data
    for child in data['data']['children']:
        post = child['data']
        posts.append({
            "title": post.get('title', ''),
            "score": post.get('score', 0),
            "sentiment": analyze_sentiment(post.get('title', '')),
            "url": post.get('url', ''),
            "timestamp": datetime.now().isoformat()
        })
    return posts

def save_to_log(posts, filename="logs.json"):
    """
    Append a list of posts to a JSON log file. Creates the file if it doesn't exist.
    
    Args:
        posts (list): List of post dictionaries to append.
        filename (str): Name of the log file (default: logs.json).
    """
    try:
        with open(filename, "r") as f:
            existing = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing = []
    
    existing.extend(posts)
    
    with open(filename, "w") as f:
        json.dump(existing, f, indent=2)

def main():
    """
    Main entry point: runs the monitoring loop for the configured number of cycles.
    Prints progress to console and saves data after each cycle.
    """
    print(f"Monitoring r/{SUBREDDIT} for {CYCLES} cycles...\n")
    all_posts = []
    
    for cycle in range(1, CYCLES + 1):
        print(f"--- Cycle {cycle} at {datetime.now().strftime('%H:%M:%S')} ---")
        
        posts = fetch_and_analyze()
        
        if posts:
            save_to_log(posts)
            # Calculate sentiment counts for this cycle
            pos = sum(1 for p in posts if p['sentiment'] == 'positive')
            neg = sum(1 for p in posts if p['sentiment'] == 'negative')
            neu = sum(1 for p in posts if p['sentiment'] == 'neutral')
            print(f"  Positive: {pos}, Negative: {neg}, Neutral: {neu}")
            all_posts.extend(posts)
        else:
            print("  No posts retrieved.")
        
        # Wait before next cycle (except after the last one)
        if cycle < CYCLES:
            print(f"  Waiting {SLEEP_SECONDS} seconds...")
            time.sleep(SLEEP_SECONDS)
    
    print(f"\nDone! Total posts analyzed: {len(all_posts)}. Data saved to logs.json")

if __name__ == "__main__":
    main()