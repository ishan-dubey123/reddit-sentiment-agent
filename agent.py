import requests
import json
import time
from datetime import datetime

SUBREDDIT = "worldnews"
POST_LIMIT = 5
SLEEP_SECONDS = 60
CYCLES = 3

POSITIVE_WORDS = ['great', 'good', 'amazing', 'excellent', 'love', 'best', 'awesome', 'fantastic', 'cool', 'nice', 'perfect', 'wonderful', 'brilliant']
NEGATIVE_WORDS = ['bad', 'terrible', 'awful', 'worst', 'hate', 'sucks', 'useless', 'trash', 'garbage', 'annoying', 'stupid', 'disappointing', 'boring']

def analyze_sentiment(text):
    text_lower = text.lower()
    pos = sum(1 for w in POSITIVE_WORDS if w in text_lower)
    neg = sum(1 for w in NEGATIVE_WORDS if w in text_lower)
    if pos > neg: return "positive"
    if neg > pos: return "negative"
    return "neutral"

def fetch_and_analyze():
    url = f"https://www.reddit.com/r/{SUBREDDIT}/new.json?limit={POST_LIMIT}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []
    data = response.json()
    posts = []
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
    try:
        with open(filename, "r") as f:
            existing = json.load(f)
    except:
        existing = []
    existing.extend(posts)
    with open(filename, "w") as f:
        json.dump(existing, f, indent=2)

def main():
    print(f"Monitoring r/{SUBREDDIT} for {CYCLES} cycles...\n")
    all_posts = []
    for cycle in range(1, CYCLES+1):
        print(f"--- Cycle {cycle} at {datetime.now().strftime('%H:%M:%S')} ---")
        posts = fetch_and_analyze()
        if posts:
            save_to_log(posts)
            pos = sum(1 for p in posts if p['sentiment']=='positive')
            neg = sum(1 for p in posts if p['sentiment']=='negative')
            neu = sum(1 for p in posts if p['sentiment']=='neutral')
            print(f"  Positive: {pos}, Negative: {neg}, Neutral: {neu}")
            all_posts.extend(posts)
        else:
            print("  No posts retrieved.")
        if cycle < CYCLES:
            print(f"  Waiting {SLEEP_SECONDS} seconds...")
            time.sleep(SLEEP_SECONDS)
    print(f"\nDone! Total posts: {len(all_posts)}. Saved to logs.json")

if __name__ == "__main__":
    main()