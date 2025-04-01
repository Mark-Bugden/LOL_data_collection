# LOL Match Scraper

A Python-based tool for scraping, processing, and saving ranked match data from the Riot Games API.

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
poetry run python src/scraping.py
```

Then run the processor:
```
poetry run python src/process_matches.py
```


## License

MIT

## Development notes:

Data flowchart available at (LucidChart)[https://lucid.app/documents/]. 
Riot developer portal (link)[https://developer.riotgames.com/docs/portal]. 
