import sys

from loguru import logger
from tqdm import tqdm


def configure_logging(log_level: str = "INFO", suppress_warnings: bool = False):
    """
    Configures the global logger.

    Args:
        log_level (str): Minimum level to log.
        suppress_warnings (bool): Whether to suppress WARNING-level messages.
    """
    logger.remove()

    # This is used so that console messages don't rewrite the tqdm progress bar
    def tqdm_sink(message):
        tqdm.write(message.rstrip())

    # This is used to re-colour the tqdm messages for easier readability
    format_str = (
        "<green>{time:HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )

    if suppress_warnings:

        def filter_no_warnings(record):
            return record["level"].name != "WARNING"

        logger.add(
            tqdm_sink,
            level=log_level.upper(),
            colorize=True,
            format=format_str,
            filter=filter_no_warnings,
        )
    else:
        logger.add(tqdm_sink, level=log_level.upper(), colorize=True, format=format_str)
