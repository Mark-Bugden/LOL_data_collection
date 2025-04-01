from riot_api.client.request import riot_request


def get_match_ids_from_puuid(
    region: str, puuid: str, start: int = 0, count: int = 20
) -> list[str]:
    """
    Retrieve recent match IDs for a player based on their PUUID.

    Args:
        region (str): The region routing value (e.g. "europe", "americas").
        puuid (str): The player's globally unique PUUID.
        start (int): The starting point in the match history (default 0).
        count (int): The number of match IDs to fetch (default 20).

    Returns:
        list[str]: A list of match IDs.
    """
    url = (
        f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    )
    params = {"start": start, "count": count}
    data = riot_request(url, params)

    return data if data else []


def get_match_data(region: str, match_id: str) -> dict:
    """
    Fetch full match details for a given match ID.

    Args:
        region (str): Region routing value (e.g. "europe", "americas").
        match_id (str): The Riot match ID string.

    Returns:
        dict: Full match data.
    """
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    data = riot_request(url)
    return data if data else {}
