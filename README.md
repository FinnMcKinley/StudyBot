# 🤖 Discord AI Bot with OpenAI & SQLAlchemy

A powerful and extensible Discord bot built in Python that integrates OpenAI for intelligent responses and uses SQLAlchemy for logging user conversations to a local database.

## ✨ Features

- Interacts with users through Discord using OpenAI's API (`$ai` command).
- Persists user messages, commands, and AI responses in a SQLite database.
- Supports:
  - Multi-message chunking for long responses.
  - Code block detection and Discord formatting.
  - User and message logging via SQLAlchemy ORM.
- Graceful shutdown with log flushing and event loop closure.
- Logging across Discord, OpenAI, and database modules.

---

## 🛠 Setup

### Prerequisites

- Python 3.10+
- [Poetry](https://python-poetry.org/) or `pip` for dependency management
- Discord Bot Token
- OpenAI API Key

### Installation

```bash
git clone https://github.com/yourusername/discord-ai-bot.git
cd discord-ai-bot
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Environment Configuration
Create a .env file in the root directory:

```env
DISCORD_TOKEN=your_discord_token_here
OPENAI_TOKEN=your_openai_key_here
```

## 💬 Usage
Run the Bot
```bash
python discord_app.py
```

## Available Commands
$hello: Replies with a simple greeting.

$ai [message]: Sends the message to OpenAI and replies with the response.

## 🧠 Database Schema
SQLite (via SQLAlchemy) with 3 main tables:

users: Stores user IDs and usernames.

messages: Tracks each message, command, and timestamp.

responses: Links to messages and stores AI-generated responses.

## 🔍 Examples
Retrieve All Users
Use the function in database.py:

```python
from database import get_all_users
print(get_all_users())
```

Search by Username
```python
from database import search_users_by_username
print(search_users_by_username("Finn"))
```

## 📂 File Structure
```bash
├── discord_app.py       # Main bot logic
├── database.py          # Database setup and query tools
├── .env                 # Environment variables
├── requirements.txt     # Dependencies
├── tmp/
│   └── app.log          # Log output
```

## 📈 Logging
Three main loggers:

Discord_API: Events and command calls

OpenAI_API: Prompt/response logging

Database: Conversation tracking and SQL interactions

Logs are written to:

tmp/app.log

Also streamed to console

## ✅ To-Do / Future Features
Session history support for ongoing context
Admin commands for log retrieval
Web dashboard (Flask or FastAPI)
New commands
Agents and chat history
Image creation
Voice Channels

## 🤝 Contributing
PRs and issues welcome. Please open an issue to discuss major changes before submitting a PR.





