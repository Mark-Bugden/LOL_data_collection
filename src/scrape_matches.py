import argparse
from itertools import product

from loguru import logger
from tqdm import tqdm

from processing.match_filters import is_valid_match
from riot_api.client.routing import get_routing
from riot_api.endpoints.ladders import get_summoner_ids_from_ladder
from riot_api.endpoints.matches import get_match_data, get_match_ids_from_puuid
from riot_api.endpoints.summoner import get_puuid_from_summoner_id
from scraping.config import SCRAPE_CONFIG
from utils.file_utils import save_raw_matches
from utils.logging_utils import configure_logging


def main():
    """Steps involved in match scraping:

    - Get list of summoner ids from first few pages of ladder
    - Use those summoner ids to get the associated puuids
    - For each puuid, get the match ids of the recent matches played by that puuid
    - Deduplicate match ids
    - For each match id, get the match data
    - Filter match data (remove short games suggesting disconnects, etc)
    - Save raw match data in batches
    """

    logger.info("Starting match scraping pipeline...")

    riot_code = SCRAPE_CONFIG["riot_code"]
    routing = get_routing(riot_code)
    logger.info(f"Using routing info: {routing}")

    summoner_ids = set()

    # Set up the progress bar for the triple for loop (tier, division, page)
    logger.info("Fetching summoner ids from ladder...")
    tier_div_page_iter = product(
        SCRAPE_CONFIG["tiers"],
        SCRAPE_CONFIG["divisions"],
        range(1, SCRAPE_CONFIG["pages_per_division"] + 1),
    )

    # Fetch the summoner IDs from the ladder pages specified in SCRAPE_CONFIG
    for tier, division, page in tqdm(
        tier_div_page_iter,
        desc="Scraping ladder",
        total=len(SCRAPE_CONFIG["tiers"])
        * len(SCRAPE_CONFIG["divisions"])
        * SCRAPE_CONFIG["pages_per_division"],
    ):
        try:
            ids = get_summoner_ids_from_ladder(
                platform=routing["platform"], tier=tier, division=division, page=page
            )
            summoner_ids.update(ids)
        except Exception as e:
            logger.warning(f"Failed to fetch ladder page {tier} {division} {page}: {e}")
            continue

    summoner_ids = list(summoner_ids)

    # Fetch PUUIDs for each summoner ID
    logger.info("Fetching puuids...")
    puuids = []
    for sid in tqdm(summoner_ids, desc="Fetching puuids"):
        try:
            puuid = get_puuid_from_summoner_id(routing["platform"], sid)
            if puuid:
                puuids.append(puuid)
        except Exception as e:
            logger.warning(f"Failed to get PUUID for Summoner ID {sid}: {e}")
            continue

    # Fetch recent match IDs for each PUUID
    logger.info("Fetching recent match ids from puuids...")
    seen_match_ids = set()
    all_match_ids = []
    for puuid in tqdm(puuids, desc="Fetching match IDs"):
        try:
            match_ids = get_match_ids_from_puuid(
                routing["region"], puuid, start=0, count=10
            )
            new_ids = [mid for mid in match_ids if mid not in seen_match_ids]
            seen_match_ids.update(new_ids)
            all_match_ids.extend(new_ids)
        except Exception as e:
            logger.warning(f"Skipping puuid {puuid} due to error: {e}")
            continue

    logger.info(f"Total unique match IDs: {len(all_match_ids)}")

    # Fetch and save match data
    batch = []
    batch_size = 100
    batch_index = 0
    logger.info(f"Fetching and saving match data in batches of size {batch_size}...")

    with tqdm(all_match_ids, desc="Fetching match data") as pbar:
        for match_id in pbar:
            try:
                match_data = get_match_data(routing["region"], match_id)
            except Exception as e:
                logger.warning(f"Skipping match {match_id} due to error: {e}")
                continue

            if match_data and is_valid_match(match_data):
                batch.append(match_data)

            if len(batch) >= batch_size:
                save_raw_matches(batch, batch_index)
                pbar.set_postfix(batch=f"{batch_index:03}", saved=len(batch))
                batch.clear()
                batch_index += 1

    # Save remaining matches (last partial batch)
    if batch:
        save_raw_matches(batch, batch_index)
        logger.info(f"Saved final batch {batch_index:03} with {len(batch)} matches.")

    logger.info("Scraping complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Riot match scraper.")
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        help="Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL). Default is INFO.",
    )
    parser.add_argument(
        "--suppress-warnings",
        action="store_true",
        help="Suppress WARNING-level log output",
    )

    args = parser.parse_args()

    configure_logging(args.log_level, suppress_warnings=args.suppress_warnings)

    main()
