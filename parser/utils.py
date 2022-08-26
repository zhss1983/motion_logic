import json
import logging

from requests import RequestException


def get_response(session, url, *args, **kwargs):
    try:
        response = session.get(url, *args, **kwargs)
        response.encoding = "utf-8"
        return response
    except RequestException as exc:
        logging.exception("Возникла ошибка при загрузке страницы %s", url, stack_info=True)
        raise RequestException from exc


def post_response(session, url, data=None, json=None, **kwargs):
    try:
        response = session.post(url, data=data, json=json, **kwargs)
        response.encoding = "utf-8"
        return response
    except RequestException as exc:
        logging.exception("Возникла ошибка при отправке страницы %s", url, stack_info=True)
        dict_dump = json.dump(kwargs)
        logging.error("url: %s\ndata = %s\ndict = %s", url, data, dict_dump)
        raise RequestException from exc


def return_json(text: str, url: str = ""):
    try:
        return json.loads(text)
    except ValueError as exc:
        logging.exception("Возникла ошибка при декодировании ответа с сайта", url, stack_info=True)
        logging.error("Текст ответа с сайта %s", text)
        raise ValueError from exc
