import datetime
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
from pandas import read_excel


def count_company_age() -> int:
    FOUNDATION_YEAR = 1920
    now_year = datetime.datetime.now().year
    return now_year - FOUNDATION_YEAR


def get_format_data_from_xlsx(file_name: str, columns: list) -> defaultdict:

    wines = read_excel(file_name, usecols=columns,
                       keep_default_na=False).to_dict(orient='record')
    wines_by_category = defaultdict(list)
    for elem in wines:
        wines_by_category[elem.pop('Категория')].append(elem)
    # for elem in wines_by_category:
    #     for el in wines_by_category[elem]:
    #         del el['Категория']
    wines_by_category = dict(sorted(wines_by_category.items(), key=lambda x: x[0]))
    return wines_by_category


def main() -> None:
    columns = [
        'Категория',
        'Название',
        'Сорт',
        'Цена',
        'Картинка',
        'Акция'
    ]
    wines_by_category = get_format_data_from_xlsx('wine3.xlsx', columns)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    rendered_page = template.render(
        company_age=count_company_age(),
        wines=wines_by_category
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('127.0.0.1', 8000), SimpleHTTPRequestHandler)
    print('start ...')
    server.serve_forever()


if __name__ == '__main__':
    main()
