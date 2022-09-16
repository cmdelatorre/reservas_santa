import logging
import re
import requests


logging.basicConfig(
    format="%(asctime)s\t%(levelname)s: %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Got it by inspecting the SMN's homepage's source code
re_prefix = "localStorage.setItem\('token',\s*[',\"]"
re_token = "[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*"
re_suffix = "[',\"]\);"
token_regex = re.compile(f"{re_prefix}({re_token}){re_suffix}")

SMN_HOME = "https://www.smn.gob.ar/"

# Got it by inspecting https://www.smn.gob.ar/pronostico
FORECAST_URL = "https://ws1.smn.gob.ar/v1/forecast/location/6177"


def get_forecast():
    """Get the weather forecast for the next 5 days in Santa Catalina."""

    try:
        resp = requests.get(SMN_HOME)
        resp.raise_for_status()
    except requests.exceptions.RequestException as err:
        logger.info(f"Couldn't get the SMN homepage for the forecast: {err}")
        return None

    jwt = token_regex.findall(resp.text)[0]
    logger.debug(f"JWT found: {jwt}")

    headers = {"Accept": "application/json", "Authorization": f"JWT {jwt}"}
    try:
        resp = requests.get(FORECAST_URL, headers=headers)
        resp.raise_for_status()
    except requests.exceptions.RequestException as err:
        logger.info(f"Couldn't get the forecast: {err}")
        return None

    response_data = resp.json()

    location = response_data["location"]["name"]
    province = response_data["location"]["province"]
    logger.info(f"Retrieved forecast for {location} ({province})")
    return response_data["forecast"]


if __name__ == "__main__":
    from pprint import pprint

    pprint(get_forecast())
