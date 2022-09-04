import json
import logging
import random
from urllib.parse import urljoin

import requests
import requests_cache
from api_service.models import ObjectType, Organisation
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .configs import configure_logging
from .constants import MAX_COUNT_RESTAURANTS, MAX_METRO_DISTANT
from .exceptions import ParserError
from .models.burgerking import BurgerKingSearchResultsSerializer
from .models.kfc import KFCSearchResultsSerializer
from .models.mcdonalds import McDonaldsSerializer
from .outputs import file_output
from .serializers import ParsingSerializer
from .utils import comma_space, create_records, end_dot


class ParserView(APIView):
    """
    Парсер ресторанов.
    Необходимо переопределить get_list_parser(session, url) и extractor(data: dict)
    """

    TITLE: str
    URL: str
    FILE_PREFIX: str

    def __init__(self):
        configure_logging()
        self.session = requests_cache.CachedSession(
            cache_name=self.FILE_PREFIX + "_cache", backend="sqlite", expire_after=60 * 60 * 24
        )
        super().__init__()

    def get_list_parser(self, url) -> list:
        """Производит запрос соответствующим методом для получения данных с API сайта."""
        raise NotImplementedError

    def extractor(self, data) -> dict:
        """Производит извлечение требуемых данных из уникальной структуры ответа API сайта"""
        raise NotImplementedError

    def parser(self, session):
        """Перебирает список организации и сохраняет его в БД. Отдаёт полученные данные далее."""
        owner = Organisation.objects.filter(title=self.TITLE).order_by("pk").first()
        if owner is None:
            object_type, _ = ObjectType.objects.get_or_create(title="Организация")
            owner = Organisation.objects.create(title=self.TITLE, address="Россия", object_type=object_type)

        data_list = self.get_list_parser(self.URL)

        result = []
        for data in data_list:
            item = self.extractor(data)
            item["object_type"] = owner.object_type
            item["owner"] = owner
            create_records(item)
            result.append(data)
        return result

    def post(self, request, format=None):
        """Загружает данные от сторонних API, обрабатывает их и дополнительно выполняет сохранеине в файл."""
        logging.info(f"Парсер ресторанов {self.TITLE} запущен!")
        with transaction.atomic():
            try:
                results = self.parser(self.session)
            except ParserError:
                serializer = ParsingSerializer({"count": 0})
                return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        if results:
            file_output(results, self.FILE_PREFIX)
        serializer = ParsingSerializer({"count": len(results)})
        logging.info(f"Парсер ресторанов {self.TITLE} завершил работу.")
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class KFCView(ParserView):
    """Парсер ресторанов KFC."""

    TITLE: str = "KFC"
    URL: str = "https://api.kfc.com/api/store/v2/store.geo_search"
    FILE_PREFIX: str = "KFC"
    FEATURE = {
        "wifi": "WiFi.",
        "breakfast": "Завтраки.",
        "driveIn": "Заезд на автомобиле.",
        "walkupWindow": "Работа только из окна.",
        "24hours": "Работает круглосуточно.",
    }
    HEADERS = {
        "accept": (
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
            "application/signed-exchange;v=b3;q=0.9"
        ),
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "max-age=0",
        "dnt": "1",
        "if-none-match": 'W/"8dca2-lo5H/vHP6lRNK854EMXJ0a8A7XE"',
        "referer": "https://www.google.com/",
        "sec-ch-ua": '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Linux",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "upgrade-insecure-requests": "1",
        "user-agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
        ),
    }
    KFC_JSON = {"coordinates": [55.7, 37.5], "radiusMeters": 100000, "showClosed": True}

    def get_list_parser(self, url):
        try:
            response = self.session.post(url, json=self.__class__.KFC_JSON, headers=self.__class__.HEADERS)
        except requests.exceptions.ConnectionError as exc:
            logging.exception("Страница не найдена URL %s", url)
            raise ParserError()
        data = json.loads(response.text)
        serializer = KFCSearchResultsSerializer(data=data)
        if serializer.is_valid():
            return serializer.data["searchResults"]
        else:
            logging.exception(
                "Ошибка валидации %s.\nURL %s\nPOST json: %s\nСтатус ответа: %s\nТекст ответа: %s",
                self.__class__.TITLE,
                url,
                self.__class__.KFC_JSON.dumps(),
                response.status_code,
                response.text,
            )
            raise ParserError()

    def extractor(self, data):
        def ru_en_choice(choice):
            return choice["ru"] if choice["ru"] else choice["en"]

        coordinate = data["store"]["contacts"]["coordinates"]["geometry"]["coordinates"]
        latitude, longitude = float(coordinate[0]), float(coordinate[1])

        description = []
        if data["distanceMeters"] < MAX_METRO_DISTANT:
            description.append(f'До ближайшего метро {data["distanceMeters"]} м.')

        for feature in data["store"]["features"]:
            if feature in self.__class__.FEATURE:
                description.append(self.__class__.FEATURE[feature])
        description = end_dot(" ".join(description))

        return {
            "description": description,
            "address": ru_en_choice(data["store"]["contacts"]["streetAddress"]),
            "title": ru_en_choice(data["store"]["title"]),
            "phone": data["store"]["contacts"]["phoneNumber"],
            "latitude": latitude,
            "longitude": longitude,
        }


class BurgerKingView(ParserView):
    """Парсер ресторанов Burger King."""

    TITLE: str = "Burger King"
    URL: str = (
        f"https://burgerkingrus.ru/api-web-front/middleware/restaurants/search?match=&limit={MAX_COUNT_RESTAURANTS}"
        "&offset=0&latitude=55.657336&longitude=37.715431"
    )
    HEADERS = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "DNT": "1",
        "Host": "burgerkingrus.ru",
        "Referer": "https://burgerkingrus.ru/restaurants",
        "sec-ch-ua": '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        "sec-ch-ua-platform": "Linux",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
        ),
        "x-burgerking-platform": "web_mobile",
    }

    FILE_PREFIX: str = "Burger_King"

    def get_list_parser(self, url):
        try:
            response = self.session.get(url, verify=False, headers=self.__class__.HEADERS)
        except requests.exceptions.ConnectionError as exc:
            logging.exception("Страница не найдена URL %s", url)
            raise ParserError()
        data = json.loads(response.text)
        serializer = BurgerKingSearchResultsSerializer(data=data)
        if serializer.is_valid():
            return serializer.data["items"]
        else:
            logging.exception(
                "Ошибка валидации %s.\nURL %s\nСтатус ответа: %s\nТекст ответа: %s",
                self.__class__.TITLE,
                url,
                response.status_code,
                response.text,
            )
            raise ParserError()

    def extractor(self, data):
        description = []
        if data["breakfast"]:
            description.append("Завтраки.")
        if data["children_party"]:
            description.append("Детские вечеринки.")
        if data["metro"]:
            description.append(end_dot(data["metro"]))
        if data["king_drive"]:
            description.append("Кинг Авто.")
        if data["parking_delivery"]:
            description.append("Вынос на парковку.")
        if data["table_delivery"]:
            description.append("Вынос к столику.")
        if data["wifi"]:
            description.append("WiFi.")
        description = end_dot(" ".join(description))
        return {
            "description": description,
            "address": end_dot(data["address"]),
            "title": end_dot("Бургер-Кинг: " + comma_space(data["name"])),
            "phone": data["phone"],
            "latitude": data["latitude"],
            "longitude": data["longitude"],
        }


class McDonaldsView(ParserView):
    """Парсер ресторанов McDonalds."""

    TITLE: str = "McDonalds"
    URL: str = "https://vkusnoitochka.ru/api/restaurant/"
    FILE_PREFIX: str = "McDonalds"
    HEADERS = {
        "accept": (
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
            "application/signed-exchange;v=b3;q=0.9"
        ),
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "max-age=0",
        "dnt": "1",
        "sec-ch-ua": '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Linux",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
        ),
    }

    def get_list_parser(self, url):
        restaurants = [urljoin(self.__class__.URL, str(count)) for count in range(1, MAX_COUNT_RESTAURANTS)]
        random.shuffle(restaurants)  # По уму ещё бы и задержку вставить, что бы не видно в логах было что парсят.
        for unit in restaurants:
            try:
                response = self.session.get(unit, verify=False, headers=self.__class__.HEADERS)
            except requests.exceptions.ConnectionError:
                logging.exception("Страница не найдена URL %s", unit)
                continue
            serializer = McDonaldsSerializer(data=json.loads(response.text))
            if serializer.is_valid():
                data = serializer.data
            else:
                logging.exception(
                    "Ошибка валидации %s.\nURL %s\nСтатус ответа: %s\nТекст ответа: %s",
                    self.__class__.TITLE,
                    unit,
                    response.status_code,
                    response.text,
                )
                continue
            if data["message"].startswith("Restaurant with id"):
                continue
            yield data

    def extractor(self, data):
        description = []
        for station in data["metro"]:
            if station["dist"] < MAX_METRO_DISTANT:
                description.append(f"Станция метро {station['name']}, расстояние {station['dist']} м.")
        for feature in data["restaurant"]["features"]:
            description.append(end_dot(feature["name"]))
        description = end_dot(" ".join(description))

        return {
            "description": description,
            "address": end_dot(comma_space(data["restaurant"]["address"])),
            "title": end_dot(comma_space(data["restaurant"]["name"])),
            "phone": data["restaurant"]["phone"],
            "latitude": 0,
            "longitude": 0,
        }
