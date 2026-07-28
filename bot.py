import logging
from telegram import Bot, ParseMode
from telegram.error import TelegramError
from config import Config
from news_scraper import NewsScraper
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot
bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)
scraper = NewsScraper()

def send_news_to_channel():
    """Fetch news and send to Telegram channel"""
    try:
        # Fetch news
        logger.info("Fetching Niger State news...")
        articles = scraper.search_niger_state_news()
        
        if not articles:
            logger.info("No positive news articles found")
            return
        
        # Format message
        message = scraper.format_news_message(articles)
        if not message:
            logger.info("No message to send")
            return
        
        # Send to Telegram channel
        logger.info(f"Sending {len(articles)} articles to channel...")
        bot.send_message(
            chat_id=Config.TELEGRAM_CHANNEL_ID,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=False
        )
        logger.info(f"Successfully sent {len(articles)} news articles to channel")
        
    except TelegramError as e:
        logger.error(f"Telegram error: {e}")
        if "bot was blocked" in str(e):
            logger.error("Bot was blocked by user or channel")
    except Exception as e:
        logger.error(f"Unexpected error in send_news_to_channel: {e}")

def test_send():
    """Test function to send a single news message"""
    logger.info("Testing news send...")
    send_news_to_channel()
    logger.info("Test completed")

if __name__ == "__main__":
    # If run directly, test the bot
    test_send()
