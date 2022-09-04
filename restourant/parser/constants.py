from pathlib import Path

BASE_DIR = Path(__file__).parent
MAX_COUNT_RESTAURANTS = 1000
MCDONALDS_URL = "https://vkusnoitochka.ru/api/restaurant/"
KFC_URL = "https://api.kfc.com/api/store/v2/store.geo_search"
KFC_JSON = {"coordinates": [55.7, 37.5], "radiusMeters": 100000, "showClosed": True}
DT_FILE_FORMAT = "%Y-%m-%d_%H-%M-%S"
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_LOG_FORMAT = "%d.%m.%Y %H:%M:%S"

MAX_METRO_DISTANT = 1000
