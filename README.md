# New Russian wine

The site of the author's wine store "New Russian wine".

## Getting Started

- Download the code
- Create **wine.xlsx** table with structure like in examlpe
- Install requirements:
```
pip install -r requirements.txt
```
- Create .env file in project dir with vars:
```
XLS_PATH=wine.xlsx
TEMLPATE_PATH=template.html
HOST=127.0.0.1
PORT=8000
```
You can use this comand for linux:
```
touch .env
```

- Start the site with the command, python 3 must be installed :
```
python3 main.py
```
- Go to the website at [http://127.0.0.1:8000 ](http://127.0.0.1:8000)

## Table

Use such structure xls table for display data on site:

| Категория | Название  | Сорт      | Цена      | Акция               |
| ----------|-----------| ----------|-----------|---------------------|
| Белые вина| Ркацители | Ркацители | 499       |                     |
| Напитки   | Чача      |           | 299       | Выгодное предложение|
| ....      | .....     | ....      | .....     | .....               |

Table examlpe: wine.xlsx 

## Project goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/)
