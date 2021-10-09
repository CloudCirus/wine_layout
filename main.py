from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pandas import read_excel
from collections import defaultdict
import datetime


def count_company_age(foundation_year: int) -> int:
    foundation_year = datetime.date(foundation_year, 1, 1).year
    now_year = datetime.datetime.now().year
    return now_year - foundation_year


def get_format_data_from_xlsx(file_name: str, columns: list) -> defaultdict:

    data = read_excel(file_name, usecols=columns, keep_default_na=False)
    data = data.to_dict(orient='record')
    format_data = defaultdict(list)
    for elem in data:
        format_data[elem['Категория']].append(elem)
    for elem in format_data:
        for el in format_data[elem]:
            del el['Категория']
    sorted_tuple = sorted(format_data.items(), key=lambda x: x[0])
    format_data = dict(sorted_tuple)
    return format_data


def main() -> None:
    columns = [
        'Категория',
        'Название',
        'Сорт',
        'Цена',
        'Картинка',
        'Акция'
    ]
    data = get_format_data_from_xlsx('wine3.xlsx', columns)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    rendered_page = template.render(
        age=count_company_age(1920),
        data=data
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('127.0.0.1', 8000), SimpleHTTPRequestHandler)
    print('start ...')
    server.serve_forever()


if __name__ == '__main__':
    main()
