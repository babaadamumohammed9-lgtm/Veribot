import requests
from bs4 import BeautifulSoup
import feedparser
import logging
from datetime import datetime, timedelta
from config import Config
import json
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.positive_keywords = [
            'development', 'achievement', 'success', 'progress', 'growth',
            'improvement', 'launch', 'inaugurate', 'commission', 'award',
            'empowerment', 'scholarship', 'investment', 'infrastructure',
            'healthcare', 'education', 'agriculture', 'youth', 'women',
            'peace', 'unity', 'celebration', 'milestone', 'record'
        ]
    
    def search_niger_state_news(self):
        """Search for Niger State news from multiple sources"""
        articles = []
        
        # Source 1: Google News RSS (if available)
        try:
            google_news_url = f"https://news.google.com/rss/search?q=Niger+State+Nigeria&hl=en-US&gl=US&ceid=US:en"
            feed = feedparser.parse(google_news_url)
            for entry in feed.entries[:10]:
                if self.is_positive_news(entry.title + " " + entry.summary):
                    articles.append({
                        'title': entry.title,
                        'summary': entry.summary,
                        'link': entry.link,
                        'published': entry.published if hasattr(entry, 'published') else '',
                        'source': 'Google News'
                    })
        except Exception as e:
            logger.error(f"Error fetching from Google News: {e}")
        
        # Source 2: Local Nigerian news sites (example with Punch)
        try:
            punch_url = "https://punchng.com/topics/niger-state/"
            response = self.session.get(punch_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                articles_found = soup.find_all('article', class_='post')
                for article in articles_found[:5]:
                    title_elem = article.find('h2')
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        link = title_elem.find('a')
                        link = link.get('href') if link else ''
                        summary = article.find('p')
                        summary = summary.get_text(strip=True) if summary else ''
                        
                        if self.is_positive_news(title + " " + summary):
                            articles.append({
                                'title': title,
                                'summary': summary,
                                'link': link,
                                'published': datetime.now().strftime('%Y-%m-%d'),
                                'source': 'Punch'
                            })
        except Exception as e:
            logger.error(f"Error fetching from Punch: {e}")
        
        # Source 3: Nigerian Tribune
        try:
            tribune_url = "https://tribuneonlineng.com/?s=niger+state"
            response = self.session.get(tribune_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                articles_found = soup.find_all('article')
                for article in articles_found[:5]:
                    title_elem = article.find('h2') or article.find('h3')
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        link = title_elem.find('a')
                        link = link.get('href') if link else ''
                        summary = article.find('p')
                        summary = summary.get_text(strip=True) if summary else ''
                        
                        if self.is_positive_news(title + " " + summary):
                            articles.append({
                                'title': title,
                                'summary': summary,
                                'link': link,
                                'published': datetime.now().strftime('%Y-%m-%d'),
                                'source': 'Nigerian Tribune'
                            })
        except Exception as e:
            logger.error(f"Error fetching from Tribune: {e}")
        
        # Remove duplicates based on title similarity
        unique_articles = []
        seen_titles = set()
        for article in articles:
            title_key = article['title'].lower()[:50]
            if title_key not in seen_titles:
                seen_titles.add(title_key)
                unique_articles.append(article)
        
        return unique_articles[:Config.MAX_ARTICLES]
    
    def is_positive_news(self, text):
        """Check if news is positive using keyword matching"""
        text_lower = text.lower()
        positive_score = sum(1 for keyword in self.positive_keywords if keyword.lower() in text_lower)
        
        # Check for negative keywords
        negative_keywords = ['crime', 'kill', 'death', 'accident', 'corruption', 
                           'scandal', 'crisis', 'violence', 'attack', 'flood', 
                           'disaster', 'tragedy', 'protests', 'strike', 'collapse']
        negative_score = sum(1 for keyword in negative_keywords if keyword.lower() in text_lower)
        
        # News is positive if positive score > negative score and positive score >= 1
        return positive_score > negative_score and positive_score >= 1
    
    def format_news_message(self, articles):
        """Format articles for Telegram message"""
        if not articles:
            return None
        
        message = "🌟 *Good News from Niger State!* 🌟\n\n"
        message += f"📰 *{len(articles)} positive updates today*\n\n"
        
        for i, article in enumerate(articles, 1):
            message += f"*{i}. {article['title']}*\n"
            if article['summary']:
                # Truncate summary if too long
                summary = article['summary'][:200] + "..." if len(article['summary']) > 200 else article['summary']
                message += f"{summary}\n"
            message += f"🔗 [Read more]({article['link']})\n"
            message += f"📌 Source: {article.get('source', 'News Source')}\n\n"
        
        message += "🤝 *Stay connected with developments in Niger State!*\n"
        message += "#NigerState #PositiveNews #Nigeria"
        
        return message
