from typing import Literal

REGION_TO_ROUTING = {
    "euw": {"platform": "euw1", "region": "europe"},
    "eune": {"platform": "eun1", "region": "europe"},
    "na": {"platform": "na1", "region": "americas"},
    "lan": {"platform": "la1", "region": "americas"},
    "las": {"platform": "la2", "region": "americas"},
    "kr": {"platform": "kr", "region": "asia"},
    "jp": {"platform": "jp1", "region": "asia"},
    "oce": {"platform": "oc1", "region": "sea"},
    # Add more if needed
}

RegionCode = Literal["euw", "eune", "na", "lan", "las", "kr", "jp", "oce"]


def get_routing(code: RegionCode) -> dict:
    """
    Get platform and region routing values from a simple region code.

    Args:
        code (RegionCode): A region code like "euw", "na", "eune", etc.

    Returns:
        dict: A dictionary with "platform" and "region" keys, or an empty
              dictionary if the code is not recognized.
    """

    if code.lower() not in REGION_TO_ROUTING:
        raise ValueError(f"Unknown region code: {code}")

    return REGION_TO_ROUTING.get(code.lower(), {})
