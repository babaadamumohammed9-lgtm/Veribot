# Niger State Positive News Telegram Bot

A Telegram bot that automatically posts positive news about Niger State, Nigeria to a Telegram channel.

## Features
- Automatically scrapes positive news about Niger State from multiple sources
- Filters out negative news using sentiment analysis
- Posts to Telegram channel every 6 hours
- Deployed on Railway with automatic updates

## Setup

### 1. Create a Telegram Bot
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` and follow the instructions
3. Copy your bot token

### 2. Create a Telegram Channel
1. Create a public channel for your news
2. Add your bot as an administrator
3. Get the channel username (e.g., `@nigerstateupdates`)

### 3. Deploy on Railway

1. Fork this repository to GitHub
2. Go to [Railway.app](https://railway.app)
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your forked repository
5. Add environment variables:
   - `TELEGRAM_BOT_TOKEN` = Your bot token
   - `TELEGRAM_CHANNEL_ID` = Your channel username (e.g., `@nigerstateupdates`)

### 4. Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/niger-state-news-bot.git
cd niger-state-news-bot

# Install dependencies
pip install -r requirements.txt

# Create .env file with your credentials
cp .env.example .env
# Edit .env with your credentials

# Run the bot
python main.py
