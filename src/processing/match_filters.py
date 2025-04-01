def is_valid_match(
    match_data: dict, min_duration: int = 300, required_queue: int = 420
) -> bool:
    """
    Checks if a match is valid for training based on basic filters.

    Args:
        match_data (dict): Raw match data from Riot API.
        min_duration (int): Minimum match duration in seconds (default: 5 min).
        required_queue (int): Required queueId (default: 420 = ranked solo).

    Returns:
        bool: True if match passes all filters, False otherwise.
    """
    try:
        info = match_data["info"]
        return (
            info["gameDuration"] >= min_duration
            and info["queueId"] == required_queue
            and len(info["participants"]) == 10
        )
    except KeyError:
        return False
