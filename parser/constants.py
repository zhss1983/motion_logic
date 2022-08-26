from pathlib import Path

BASE_DIR = Path(__file__).parent
MAX_COUNT_RESTAURANTS = 1000
BURGER_KING_URL = (
    f"https://burgerkingrus.ru/api-web-front/middleware/restaurants/search?match=&limit={MAX_COUNT_RESTAURANTS}"
    "&offset=0&latitude=55.7&longitude=37.6"
)
MCDONALDS_URL = "https://vkusnoitochka.ru/api/restaurant/"
KFC_URL = "https://api.kfc.com/api/store/v2/store.geo_search"
KFC_JSON = {"coordinates": [55.7, 37.5], "radiusMeters": 10000, "showClosed": True}
DT_FILE_FORMAT = "%Y-%m-%d_%H-%M-%S"
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_LOG_FORMAT = "%d.%m.%Y %H:%M:%S"
