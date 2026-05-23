# AutoFilterBot

A powerful Telegram auto-filter bot for indexing and searching media files in channels and groups.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Pyrogram](https://img.shields.io/badge/Pyrogram-2.0+-orange.svg)](https://pyrogram.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-4.0+-green.svg)](https://www.mongodb.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Features

### Core Features
- **Auto Filter** - Automatically index and search files from connected channels
- **Manual Filter** - Create custom keyword-based filters
- **IMDB Integration** - Fetch movie/show information from IMDB
- **Inline Search** - Search files directly in any chat using inline mode
- **Spell Check** - Suggests corrections for misspelled queries

### Admin Features
- **Broadcast** - Send messages to all users/groups
- **Statistics** - View detailed bot and database statistics
- **User Management** - Ban/unban users, enable/disable groups
- **File Management** - Delete specific files or clear entire index

### Group Features
- **Connection System** - Manage groups from PM
- **Custom Templates** - Set custom IMDB templates per group
- **Welcome Messages** - Customizable welcome messages
- **Button Lock** - Restrict file buttons to requester only

### Additional Features
- **URL Shortener** - Integrate with link shortening services
- **File Protection** - Restrict content forwarding
- **Custom Captions** - Set custom file captions
- **Auto Delete** - Automatically delete filter messages

## Quick Start

### Prerequisites
- Python 3.10 or higher
- MongoDB database
- Telegram Bot Token
- Telegram API credentials

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/DevilServers/AutoFilterbot.git
cd AutoFilterbot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your values
```

4. **Run the bot**
```bash
python bot.py
```

## Configuration

### Required Variables

| Variable | Description |
|----------|-------------|
| `BOT_TOKEN` | Telegram bot token from [@BotFather](https://t.me/BotFather) |
| `API_ID` | Telegram API ID from [my.telegram.org](https://my.telegram.org) |
| `API_HASH` | Telegram API Hash from [my.telegram.org](https://my.telegram.org) |
| `ADMINS` | Space-separated list of admin user IDs |
| `DATABASE_URL` | MongoDB connection URI |
| `DATABASE_NAME` | MongoDB database name |
| `LOG_CHANNEL` | Channel ID for logging bot activities |

### Optional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CHANNELS` | - | Source channels for auto-indexing (space-separated) |
| `AUTH_CHANNEL` | - | Force subscribe channel ID |
| `SUPPORT_CHAT` | - | Support group username (without @) |
| `PICS` | - | Space-separated Telegraph image URLs for start message |
| `IMDB` | True | Enable IMDB integration |
| `SINGLE_BUTTON` | True | Use single button layout |
| `PROTECT_CONTENT` | False | Restrict content forwarding |
| `SHORT_URL` | - | URL shortener domain |
| `SHORT_API` | - | URL shortener API key |

See `.env.example` for the complete list of configuration options.

## Deployment

### Heroku
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

### Railway
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template)

### Koyeb
[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy)

### Render
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### Docker
```bash
docker build -t autofilterbot .
docker run -d --env-file .env autofilterbot
```

## Commands

### User Commands
| Command | Description |
|---------|-------------|
| `/start` | Start the bot |
| `/help` | Show help message |
| `/about` | About the bot |

### Admin Commands
| Command | Description |
|---------|-------------|
| `/stats` | Show bot statistics |
| `/broadcast` | Broadcast message to users |
| `/users` | List all users |
| `/chats` | List all chats |
| `/ban_user` | Ban a user |
| `/unban_user` | Unban a user |
| `/logs` | Get recent logs |

### Group Commands
| Command | Description |
|---------|-------------|
| `/settings` | Configure group settings |
| `/connect` | Connect group to PM |
| `/disconnect` | Disconnect from group |
| `/filter` | Add manual filter |
| `/filters` | List all filters |
| `/del` | Delete a filter |
| `/delall` | Delete all filters |
| `/set_template` | Set IMDB template |

### Index Commands
| Command | Description |
|---------|-------------|
| `/index` | Index a channel |
| `/channel` | List indexed channels |
| `/delete` | Delete specific file |
| `/deleteall` | Delete all indexed files |

## Project Structure

```
AutoFilterbot/
├── bot.py              # Main bot entry point
├── info.py             # Configuration loader
├── Script.py           # Bot messages and templates
├── utils.py            # Utility functions
├── database/           # Database modules
│   ├── ia_filterdb.py  # File indexing database
│   ├── users_chats_db.py # Users and chats database
│   ├── connections_mdb.py # Connections database
│   ├── filters_mdb.py  # Manual filters database
│   └── gfilters_mdb.py # Global filters database
├── plugins/            # Bot command handlers
│   ├── commands.py     # Basic commands
│   ├── pm_filter.py    # PM filter handler
│   ├── group_filter.py # Group filter handler
│   ├── index.py        # Indexing commands
│   ├── connection.py   # Connection commands
│   ├── broadcast.py    # Broadcast commands
│   └── stats.py        # Statistics commands
└── utils/              # Utility modules
    └── health.py       # Health check utilities
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

- **Telegram Group**: [@DevilServers](https://t.me/DevilServers)
- **Issues**: [GitHub Issues](https://github.com/DevilServers/AutoFilterbot/issues)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Pyrogram](https://pyrogram.org/) - Telegram MTProto API framework
- [Motor](https://motor.readthedocs.io/) - Async MongoDB driver
- [Cinemagoer](https://cinemagoer.github.io/) - IMDB data access

---

**Made with love by [Devil TG](https://t.me/DevilServers)**
