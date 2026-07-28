import schedule
import time
import logging
from datetime import datetime
from bot import send_news_to_channel
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scheduled_news_post():
    """Function to run scheduled news posting"""
    logger.info(f"Running scheduled news post at {datetime.now()}")
    try:
        send_news_to_channel()
        logger.info("Scheduled news post completed successfully")
    except Exception as e:
        logger.error(f"Error in scheduled news post: {e}")

def start_scheduler():
    """Start the scheduler"""
    # Schedule posts every X hours
    schedule.every(Config.POST_INTERVAL_HOURS).hours.do(scheduled_news_post)
    
    # Also run on startup
    scheduled_news_post()
    
    logger.info(f"Scheduler started. Will post every {Config.POST_INTERVAL_HOURS} hours")
    
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user")
            break
        except Exception as e:
            logger.error(f"Scheduler error: {e}")
            time.sleep(60)
