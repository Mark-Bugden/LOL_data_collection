from riot_api.client.request import riot_request


def get_puuid_from_riot_id(region: str, game_name: str, tagline: str) -> str | None:
    """
    Retrieve the PUUID for a player using their Riot ID.

    Args:
        region (str): Regional routing value (e.g. "europe", "americas").
        game_name (str): The player's Riot display name.
        tagline (str): The player's Riot tagline (e.g. "EUW").

    Returns:
        str | None: The player's PUUID, or None if not found.

    Notes:
        This uses the Riot Account API (regional route).
    """
    url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tagline}"
    data = riot_request(url)
    return data.get("puuid") if data else None


def get_summoner_id_from_puuid(platform: str, puuid: str) -> str | None:
    """
    Retrieve the Summoner ID for a player using their PUUID.

    Args:
        platform (str): Platform routing value (e.g. "euw1", "na1").
        puuid (str): The globally unique Riot PUUID.

    Returns:
        str | None: The player's Summoner ID, or None if not found.

    Notes:
        This uses the Summoner API (platform route).
    """
    url = f"https://{platform}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
    data = riot_request(url)
    return data.get("id") if data else None


def get_puuid_from_summoner_id(platform: str, summoner_id: str) -> str | None:
    """
    Retrieve the PUUID for a player using their Summoner ID.

    Args:
        platform (str): Platform routing value (e.g. "euw1", "na1").
        summoner_id (str): The LoL-specific internal Summoner ID.

    Returns:
        str | None: The player's PUUID, or None if not found.

    Notes:
        This uses the Summoner API (platform route).
    """
    url = (
        f"https://{platform}.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}"
    )
    data = riot_request(url)
    return data.get("puuid") if data else None
