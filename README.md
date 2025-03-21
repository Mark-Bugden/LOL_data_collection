# LOL Match Scraper

A Python-based tool for scraping ranked match data from the Riot Games API using player Riot IDs.

## Features
- Resolve Riot ID to PUUID and Summoner ID
- Fetch match history and match details
- Handles rate limits and retries
- Stores match data locally for analysis

## Requirements
- Python 3.12+
- [Poetry](https://python-poetry.org/)
- Riot API key (stored in `.env`)

## Setup

```
poetry install
```

Create a `.env` file with:

```
RIOT_API_KEY=your-api-key-here
```

## Usage

Run the scraper:

```
poetry run python src/main.py
```

## License

MIT
