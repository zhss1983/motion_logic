import logging
import random
from urllib.parse import urljoin

import requests_cache
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (
    BURGER_KING_URL,
    KFC_JSON,
    KFC_URL,
    MCDONALDS_URL,
)
from outputs import control_output
from utils import get_response, post_response, return_json


def burger_king(session):
    response = get_response(session, BURGER_KING_URL, verify=False)
    return return_json(response.text, BURGER_KING_URL)


def mcdonalds(session):
    restaurants = [urljoin(MCDONALDS_URL, str(count)) for count in range(1, 1000)]
    random.shuffle(restaurants)  # По уму ещё бы и задержку вставить, что бы не видно в логах было что парсят.
    result = []
    for unit in tqdm(restaurants):
        response = get_response(session, unit, verify=False)
        data = return_json(response.text, unit)
        if data.get("message", "").startswith("Restaurant with id"):
            continue
        result.append(data)
    return result


def kfc(session):
    response = post_response(session, KFC_URL, json=KFC_JSON)
    return return_json(response.text, KFC_URL)


MODE_TO_FUNCTION = {
    "burger-king": burger_king,
    "mcdonalds": mcdonalds,
    "kfc": kfc,
}


def main():
    configure_logging()
    logging.info("Парсер запущен!")
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info("Аргументы командной строки: %s", args)
    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()
    results = MODE_TO_FUNCTION[args.mode](session)
    if results:
        control_output(results, args)
    logging.info("Парсер завершил работу.")


if __name__ == "__main__":
    main()
