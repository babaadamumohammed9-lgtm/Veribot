import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')
    NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')
    
    # Keywords for filtering Niger State news
    KEYWORDS = [
        'niger state', 'minna', 'bida', 'suleja', 'kontagora',
        'niger nigeria', 'niger state government'
    ]
    
    # Posting schedule (in hours)
    POST_INTERVAL_HOURS = 6
    
    # Maximum news articles per fetch
    MAX_ARTICLES = 5
