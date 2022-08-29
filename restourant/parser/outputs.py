import logging
from datetime import datetime as dt
from pprint import pformat

from .constants import BASE_DIR, DT_FILE_FORMAT


def file_output(results, prefix):
    results_dir = BASE_DIR / "results"
    results_dir.mkdir(exist_ok=True)
    file_name = f"{prefix}_{dt.now().strftime(DT_FILE_FORMAT)}.txt"
    file_path = results_dir / file_name
    with open(file_path, mode="w", encoding="utf-8") as file:
        file.write(pformat(results))
    logging.info("Файл с результатами был сохранён: %s", file_path)
