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
