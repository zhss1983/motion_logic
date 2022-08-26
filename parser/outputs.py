import logging
from datetime import datetime as dt

from pprint import pprint, pformat

from constants import BASE_DIR, DT_FILE_FORMAT


def file_output(results, cli_args):
    results_dir = BASE_DIR / "results"
    results_dir.mkdir(exist_ok=True)
    file_name = f"{cli_args.mode}_{dt.now().strftime(DT_FILE_FORMAT)}.txt"
    file_path = results_dir / file_name
    with open(file_path, mode="w", encoding="utf-8") as file:
        file.write(pformat(results))
    logging.info("Файл с результатами был сохранён: %s", file_path)


def default_output(results, _=None):
    pprint(results)


OUTPUT = {
    "file": file_output,
    None: default_output,
}


def control_output(results, cli_args):
    OUTPUT[cli_args.output](results, cli_args)
