import httpx
from typing import Any

from src.config import COUNTRIES_API_BASE
from src.logger import logger

_client = httpx.Client(timeout=10.0)


def fetch_country(name: str) -> dict[str, Any]:
    """
    Fetch country data from REST Countries API.

    Args:
        name: Country name to search for.

    Returns:
        Dict with country data fields, or error dict.
    """
    url = f"{COUNTRIES_API_BASE}/name/{name}"
    logger.info(f"Fetching country data: {url}")

    try:
        response = _client.get(url)

        if response.status_code == 404:
            return {"error": f"Country '{name}' not found."}

        response.raise_for_status()
        results = response.json()

        if not results:
            return {"error": f"No data returned for '{name}'."}

        # Take the first (best) match
        country = results[0]

        currencies = country.get("currencies", {})
        currency_list = [
            {"code": code, "name": info.get("name"), "symbol": info.get("symbol")}
            for code, info in currencies.items()
        ]

        languages = country.get("languages", {})
        idd = country.get("idd", {})
        calling_code = f"{idd.get('root', '')}{(idd.get('suffixes', ['']))[0]}" if idd else None

        data = {
            "name": country.get("name", {}).get("common"),
            "official_name": country.get("name", {}).get("official"),
            "capital": country.get("capital", []),
            "population": country.get("population"),
            "area_km2": country.get("area"),
            "region": country.get("region"),
            "subregion": country.get("subregion"),
            "currencies": currency_list,
            "languages": list(languages.values()),
            "timezones": country.get("timezones", []),
            "borders": country.get("borders", []),
            "flag_emoji": country.get("flag"),
            "continent": country.get("continents", []),
            "independent": country.get("independent"),
            "un_member": country.get("unMember"),
            "calling_code": calling_code,
            "tld": country.get("tld", []),
            "driving_side": country.get("car", {}).get("side"),
            "landlocked": country.get("landlocked"),
            "lat_lng": country.get("latlng"),
        }

        logger.info(f"Fetched data for: {data['name']}")
        return data

    except httpx.TimeoutException:
        logger.error(f"Timeout fetching country: {name}")
        return {"error": f"Request timed out while fetching data for '{name}'."}
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error fetching country: {e}")
        return {"error": f"API error: {e.response.status_code}"}
    except Exception as e:
        logger.error(f"Unexpected error fetching country: {e}")
        return {"error": f"Failed to fetch country data: {str(e)}"}
