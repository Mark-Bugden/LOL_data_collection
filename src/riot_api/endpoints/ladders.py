from riot_api.client.request import riot_request


def get_summoner_ids_from_ladder(
    platform: str, tier: str = "DIAMOND", division: str = "IV", page: int = 1
) -> list[str]:
    """
    Fetch a list of Summoner IDs from the ranked Solo Queue ladder.

    Args:
        platform (str): Platform routing value (e.g. "euw1").
        tier (str): Tier to query (e.g. "DIAMOND", "MASTER").
        division (str): Division within tier (e.g. "I", "II", "III", "IV").
        page (int): Page number for pagination (starts from 1).

    Returns:
        list[str]: A list of Summoner IDs.
    """
    url = (
        f"https://{platform}.api.riotgames.com/lol/league/v4/"
        f"entries/RANKED_SOLO_5x5/{tier}/{division}?page={page}"
    )
    data = riot_request(url)
    if not data:
        return []

    return [entry["summonerId"] for entry in data if "summonerId" in entry]
