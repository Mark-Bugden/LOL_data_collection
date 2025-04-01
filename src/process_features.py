import argparse
import csv
import json
from pathlib import Path

from loguru import logger
from tqdm import tqdm

from processing.config import feature_config
from processing.match_features import extract_team_features
from processing.match_filters import is_valid_match
from utils.logging_utils import configure_logging


def main():
    """Steps involved in feature processing:

    - Load raw match data from jsonl batch files
    - Filter matches (e.g. short games, wrong queue type)
    - Extract team-level features based on config
    - Save processed features to CSV
    """

    logger.info("Starting match feature processing pipeline...")

    raw_data_dir = Path("data/raw_matches")
    output_path = Path("data/processed_matches/team_features.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Reading raw matches from: {raw_data_dir}")
    logger.info(f"Processed feature output path: {output_path}")

    num_rows_written = 0
    fieldnames = None

    with open(output_path, "w", newline="", encoding="utf-8") as out_file:
        writer = None

        for file in tqdm(
            sorted(raw_data_dir.glob("*.jsonl")), desc="Processing batch files..."
        ):
            logger.debug(f"Processing file: {file.name}")
            with open(file, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        match_data = json.loads(line)
                    except json.JSONDecodeError:
                        logger.warning(f"Skipping malformed JSON line in {file.name}")
                        continue

                    if not is_valid_match(match_data):
                        continue

                    team_rows = extract_team_features(match_data, feature_config)

                    if team_rows:
                        if writer is None:
                            fieldnames = team_rows[0].keys()
                            writer = csv.DictWriter(out_file, fieldnames=fieldnames)
                            writer.writeheader()

                        writer.writerows(team_rows)
                        num_rows_written += len(team_rows)

    if num_rows_written > 0:
        logger.info(f"Saved {num_rows_written} team feature rows to {output_path}")
    else:
        logger.warning("No valid matches found. Nothing written.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract features from raw Riot match data."
    )
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
