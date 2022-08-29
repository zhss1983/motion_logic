import json
import logging

import requests
from api_service.models import ObjectType, Organisation, Owner, Phone


def get_response(session, url, *args, **kwargs):
    try:
        response = session.get(url, *args, **kwargs)
        response.encoding = "utf-8"
        return response
    except requests.RequestException as exc:
        logging.exception("Возникла ошибка при загрузке страницы %s", url, stack_info=True)
        raise requests.RequestException from exc


def post_request(session, url, data=None, json=None, **kwargs):
    try:
        response = session.post(url, data=data, json=json, **kwargs)
        response.encoding = "utf-8"
        return response
    except requests.RequestException as exc:
        logging.exception("Возникла ошибка при отправке страницы %s", url, stack_info=True)
        dict_dump = json.dump(kwargs)
        logging.error("url: %s\ndata = %s\ndict = %s", url, data, dict_dump)
        raise requests.RequestException from exc


def return_json(text: str, url: str = ""):
    try:
        return json.loads(text)
    except ValueError as exc:
        logging.exception("Возникла ошибка при декодировании ответа с сайта", url, stack_info=True)
        logging.error("Текст ответа с сайта %s", text)
        raise ValueError from exc


def end_dot(text: str) -> str:
    return text.strip(". \n\t") + "."


def comma_space(text: str) -> str:
    return ", ".join(map(lambda word: word.strip(), text.split(",")))


def create_records(item):

    organisation, _ = Organisation.objects.get_or_create(
        title=item["title"],
        object_type=item["object_type"],
        address=item["address"],
        latitude=item["latitude"],
        longitude=item["longitude"],
        description=item["description"],
    )
    Owner.objects.get_or_create(
        owner=item["owner"],
        organisation=organisation,
    )
    Phone.objects.get_or_create(
        phone=item["phone"],
        organisation=organisation,
    )
