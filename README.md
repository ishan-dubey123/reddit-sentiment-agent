# Reddit Sentiment Analysis Agent

A Python-based agent that continuously monitors Reddit for new posts, analyzes sentiment using keyword matching, and logs results for business insights.

## Features

- Fetches latest posts from any subreddit using Reddit's public JSON API
- Analyzes sentiment (positive/negative/neutral) based on title keywords
- Runs in continuous monitoring cycles with configurable intervals
- Saves all data to a structured JSON log file
- Handles errors gracefully (network issues, missing data)
- Fully documented code with docstrings and comments

## Setup & Run

1. Install Python 3.7 or higher
2. Install the required dependency: pip install -r requirements.txt 
3. Run the agent : python agent.py

## Architecture

[Manual Run] -> [Reddit API] -> [JSON Log]

Components:
- fetch_and_analyze() : calls Reddit API
- analyze_sentiment() : checks keywords
- save_to_log() : saves to logs.json
- main() : runs the loop

## Business Value

This agent helps businesses:
- Monitor brand sentiment in real time on social media
- Detect emerging trends or customer complaints early
- Make data-driven decisions with low cost (no API fees)

Use cases: market research, PR monitoring, competitor analysis.

## Self-Assessment

**Trade-offs:**
- Keyword matching vs. ML: Chosen for speed and zero dependencies; may miss sarcasm
- Public JSON API vs. official API: Avoids authentication friction; suitable for small-scale use
- Local JSON storage vs. database: Simpler for demo; can be upgraded later

**Future improvements:**
- Integrate Hugging Face transformers for deeper sentiment
- Add database (PostgreSQL) for long-term storage
- Deploy as scheduled cloud function (AWS Lambda, GitHub Actions)

## Code Documentation

The `agent.py` script includes:
- Module-level docstring explaining the agent
- Docstrings for every function (arguments, return values, behavior)
- Inline comments for non-obvious logic
- Error handling for network and file operations