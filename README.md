# Clips Courier

[![EO principles respected here](https://www.elegantobjects.org/badge.svg)](https://www.elegantobjects.org)

A private Telegram bot that delivers short videos into the chat. Send it a link to a TikTok, Instagram Reels, or X videos — it downloads the clip with [yt-dlp](https://github.com/yt-dlp/yt-dlp) and sends it back as a regular Telegram video.

The bot is private by default: only the owner and the people the owner adds ("friends") can download videos.

## How It Works

1. You send `/d <link>` to the bot.
2. The bot checks that you are the owner or a friend.
3. It downloads the video to a temporary folder and sends it to the chat.
4. The temporary file is deleted right after.

## Commands

| Command | Who | What it does |
|---|---|---|
| `/s` | Everyone | Show the welcome message |
| `/h` | Everyone | Show help |
| `/d <link>` | Owner and friends | Download the video and send it to the chat |
| `/dm <link>` | Owner and friends | Same as `/d`, plus a caption with the description, author, and platform |
| `/f @username` | Owner only | Add a friend |
| `/fl` | Owner only | Show the friend list |
| `/kf @username` | Owner only | Remove a friend |

## Setup

You need two things:

- A bot token — create a bot with [@BotFather](https://t.me/BotFather) in Telegram.
- Your Telegram user ID — ask [@userinfobot](https://t.me/userinfobot) or a similar bot.

### Configuration

All settings come from environment variables (see `.env.example`):

| Variable | Required | Description |
|---|---|---|
| `BOT_KEY` | Yes | Bot token from BotFather |
| `OWNER_ID` | Yes | Telegram user ID of the owner |
| `BOT_NAME` | No | Display name shown in the welcome and help messages |
| `DB_PATH` | No | Path to the SQLite database file (default: `courier.db`) |

### Run with Docker

The image is published on Docker Hub automatically on every tagged release, so there is nothing to build:

```sh
docker run -d \
  -e BOT_KEY=123456:your-token \
  -e OWNER_ID=123456789 \
  -e DB_PATH=/data/courier.db \
  -v courier-data:/data \
  lymagics/clips-courier
```

The volume keeps the friend list when the container is recreated.

### Run Locally

Requires Python 3.12+ and [uv](https://github.com/astral-sh/uv).

```sh
uv sync
cp .env.example .env   # fill in BOT_KEY and OWNER_ID
make bot
```

## Development

```sh
make unit     # run unit tests with coverage
make black    # format code
make flake8   # lint with flake8
make ruff     # lint with ruff
```

## License

[MIT](LICENSE)
