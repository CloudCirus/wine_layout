import argparse
import datetime
import logging
import os
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
from pandas import read_excel
from dotenv import load_dotenv


def count_company_age() -> int:
    FOUNDATION_YEAR = 1920
    now_year = datetime.datetime.now().year

    return now_year - FOUNDATION_YEAR


def get_format_data_from_xlsx(file_name: str, columns: list, logging: logging) -> defaultdict:
    try:
        wines = read_excel(file_name, usecols=columns,
                           keep_default_na=False).to_dict(orient='records')
    except TypeError and UnboundLocalError and FileNotFoundError as ex:
        logging.exception('Reading xls file problem\n')
    wines_by_category = defaultdict(list)
    for elem in wines:
        wines_by_category[elem.pop('Категория')].append(elem)

    wines_by_category = dict(
        sorted(wines_by_category.items(), key=lambda x: x[0]))

    return wines_by_category


def main() -> None:
    load_dotenv()
    xls_path = os.getenv('XLS_PATH')
    template_path = os.getenv('TEMLPATE_PATH')
    host = os.getenv('HOST')
    port = os.getenv('PORT')

    parser = argparse.ArgumentParser(
        description='display wines from xlsx on web-layout'
    )
    parser.add_argument('--file_path', default=xls_path,
                        help='path to xlsx file', type=str)
    parser.add_argument('--template_path', default=template_path,
                        help='path to template fo rendering', type=str)
    parser.add_argument('--host', default=host,
                        help='server host', type=str)
    parser.add_argument('--port', default=port,
                        help='server port', type=int)
    args = parser.parse_args()

    logging.basicConfig(filename='sample.log', level=logging.INFO)
    log = logging.getLogger('main')

    columns = [
        'Категория',
        'Название',
        'Сорт',
        'Цена',
        'Картинка',
        'Акция'
    ]
    wines_by_category = get_format_data_from_xlsx(
        args.file_path, columns, logging=log)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template(args.template_path)
    rendered_page = template.render(
        company_age=count_company_age(),
        wines_by_category=wines_by_category.items(),
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer((args.host, args.port), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
