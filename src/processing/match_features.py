def extract_team_features(match_data: dict, config: dict) -> list[dict]:
    """
    Extracts team-level features from raw match data.

    Args:
        match_data (dict): Raw match data from the Riot API.
        config (dict): Feature config flags.

    Returns:
        list[dict]: One dict per team, with extracted features.
    """
    info = match_data["info"]
    match_id = match_data["metadata"]["matchId"]
    participants = info["participants"]

    teams = {100: [], 200: []}
    for p in participants:
        teams[p["teamId"]].append(p)

    rows = []
    for team_id, players in teams.items():
        row = {}

        if config.get("include_match_id", True):
            row["match_id"] = match_id

        if config.get("include_team_id", True):
            row["team_id"] = team_id

        if config.get("include_champions", True):
            row["champions"] = sorted([p["championName"] for p in players])

        if config.get("include_outcome", True):
            row["win"] = int(players[0]["win"])  # all players share the same 'win'

        if config.get("include_summoner_spells", True):
            row["spells"] = sorted(
                [(p["summoner1Id"], p["summoner2Id"]) for p in players]
            )

        if config.get("include_runes", True):
            row["primary_styles"] = sorted(
                [p["perks"]["styles"][0]["style"] for p in players]
            )
            row["keystones"] = sorted(
                [p["perks"]["styles"][0]["selections"][0]["perk"] for p in players]
            )

        if config.get("include_game_mode", True):
            row["game_mode"] = info.get("gameMode")

        if config.get("include_queue_id", True):
            row["queue_id"] = info.get("queueId")

        if config.get("include_map_id", True):
            row["map_id"] = info.get("mapId")

        rows.append(row)

    return rows
