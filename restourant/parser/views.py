import logging
import random
from urllib.parse import urljoin

import requests_cache
from api_service.models import ObjectType, Organisation
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .configs import configure_logging
from .constants import BURGER_KING_URL, KFC_JSON, KFC_URL, MAX_COUNT_RESTAURANTS, MAX_METRO_DISTANT, MCDONALDS_URL
from .outputs import file_output
from .serializers import ParsingSerializer
from .utils import comma_space, create_records, end_dot, get_response, post_request, return_json


class ParserView(APIView):
    """
    Парсер ресторанов.
    Необходимо переопределить get_list_parser(session, url) и extractor(data: dict)
    """

    TITLE: str
    URL: str
    FILE_PREFIX: str

    def get_list_parser(self, session, url) -> list:
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

        data_list = self.get_list_parser(session, self.URL)

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
        configure_logging()
        logging.info(f"Парсер ресторанов {self.TITLE} запущен!")
        session = requests_cache.CachedSession(
            cache_name=self.FILE_PREFIX + "_cache", backend="sqlite", expire_after=60 * 60 * 24
        )

        with transaction.atomic():
            results = self.parser(session)

        if results:
            file_output(results, self.FILE_PREFIX)

        serializer = ParsingSerializer({"count": len(results)})
        logging.info(f"Парсер ресторанов {self.TITLE} завершил работу.")

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class KFCView(ParserView):
    """Парсер ресторанов KFC."""

    TITLE: str = "KFC"
    URL: str = KFC_URL
    FILE_PREFIX: str = "KFC"

    def get_list_parser(self, session, url):
        restaurant_response = post_request(session, url, json=KFC_JSON)
        return return_json(restaurant_response.text, url).get("searchResults", [])

    def extractor(self, data):
        def ru_en_choice(choice):
            return choice.get("ru", choice.get("en", ""))

        store = data.get("store", {})

        contacts = store.get("contacts", {})

        address = ru_en_choice(contacts.get("streetAddress", {}))

        coordinate = contacts.get("coordinates", {}).get("geometry", {}).get("coordinates", (0, 0))
        latitude, longitude = float(coordinate[0]), float(coordinate[1])

        phone = contacts.get("phoneNumber", "")

        title = ru_en_choice(store.get("title", {}))

        description = []
        dist = int(data.get("distanceMeters", MAX_METRO_DISTANT))
        if dist < MAX_METRO_DISTANT:
            description.append(f"До ближайшего метро {dist} м.")
        features = store.get("features", [])
        match features:
            case "wifi", _:
                description.append("WiFi.")
            case "breakfast", _:
                description.append("Завтраки.")
            case "driveIn", _:
                description.append("Заезд на автомобиле.")
            case "walkupWindow", _:
                description.append("Работа только из окна.")
            case "24hours", _:
                description.append("Работает круглосуточно.")
        description = end_dot(" ".join(description))

        return {
            "description": description,
            "address": address,
            "title": title,
            "phone": phone,
            "latitude": latitude,
            "longitude": longitude,
        }


class BurgerKingView(ParserView):
    """Парсер ресторанов Burger King."""

    TITLE: str = "Burger King"
    URL: str = BURGER_KING_URL
    FILE_PREFIX: str = "Burger_King"

    def get_list_parser(self, session, url):
        response = get_response(session, url, verify=False)
        return return_json(response.text, url).get("items", [])

    def extractor(self, data):
        address = end_dot(comma_space(data.get("address", "")))
        latitude = float(data.get("latitude", 0))
        longitude = float(data.get("longitude", 0))
        phone = data.get("phone", "")
        title = end_dot("Бургер-Кинг: " + comma_space(data.get("name", "")))
        description = []
        if data.get("breakfast", False):
            description.append("Завтраки.")
        if data.get("children_party", False):
            description.append("Детские вечеринки.")
        metro = data.get("metro", False)
        if metro:
            description.append(end_dot(metro))
        if data.get("king_drive", False):
            description.append("Кинг Авто.")
        if data.get("parking_delivery", False):
            description.append("Вынос на парковку.")
        if data.get("table_delivery", False):
            description.append("Вынос к столику.")
        if data.get("wifi", False):
            description.append("WiFi.")
        description = end_dot(" ".join(description))
        return {
            "description": description,
            "address": address,
            "title": title,
            "phone": phone,
            "latitude": latitude,
            "longitude": longitude,
        }


class McDonaldsView(ParserView):
    """Парсер ресторанов McDonalds."""

    TITLE: str = "McDonalds"
    URL: str = MCDONALDS_URL
    FILE_PREFIX: str = "McDonalds"

    def get_list_parser(self, session, url):
        restaurants = [urljoin(MCDONALDS_URL, str(count)) for count in range(1, MAX_COUNT_RESTAURANTS)]
        random.shuffle(restaurants)  # По уму ещё бы и задержку вставить, что бы не видно в логах было что парсят.
        for unit in restaurants:
            response = get_response(session, unit, verify=False)
            data = return_json(response.text, unit)
            if data.get("message", "").startswith("Restaurant with id"):
                continue
            yield data

    def extractor(self, data):
        metro = data.get("metro", [])
        restaurant = data.get("restaurant", {})
        features = restaurant.get("features", [])
        description = []
        for station in metro:
            dist = station.get("dist", MAX_METRO_DISTANT)
            if dist < MAX_METRO_DISTANT:
                name = station.get("name", "")
                description.append(f"Станция метро {name}, расстояние {dist} м.")
        for feature in features:
            name = feature.get("name", "")
            description.append(end_dot(name))
        description = end_dot(" ".join(description))
        address = end_dot(comma_space(restaurant.get("address", "")))
        title = end_dot(comma_space(restaurant.get("name", "")))
        phone = restaurant.get("phone", "")
        latitude = 0
        longitude = 0
        return {
            "description": description,
            "address": address,
            "title": title,
            "phone": phone,
            "latitude": latitude,
            "longitude": longitude,
        }
