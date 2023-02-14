# Импортируем нужные библиотеки

import requests as req
from bs4 import BeautifulSoup as bs
import httplib2
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import creds

url = 'https://confluence.hflabs.ru/pages/viewpage.action?pageId=1181220999'  # Наша ссылка,которую нужно парсить
page = req.get(url)  # Создание объекта страницы,запрос на разрешение
soup = bs(page.text, 'lxml')  # Объект html-кода
table1 = soup.find('div', id='main-content')  # Поиск таблицы в тегах HTML
headers = []  # Список для заголовков
for i in table1.find_all('th'):  # Ищем в HTML тегах таблицы тег для заголовков,добавляем в headers
    title = i.text
    headers.append(title)

rows = []  # Список строк таблицы

for j in table1.find_all('tr')[1:]:  # Ищем тег tr

    row_data = j.find_all('td')  # в теге tr ищем тег td
    row = [i.text for i in row_data]  # находим строку
    rows.append(row)  # добавляем в rows


# '1jOSr4MW2mmnXJpI1qulDiTVTJaB7rJ4RMYzu5BvPOEk'

# Далее идет подключение к google sheets
def get_service_simple():
    return build('sheets', 'v4', developerKey=creds.api_key)


def get_service_sacc():
    creds_json = 'testtask.json'  # json файл для подключения к google sheets
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())
    return build('sheets', 'v4', http=creds_service)


sheet = get_service_sacc().spreadsheets()

sheet_id = '1jOSr4MW2mmnXJpI1qulDiTVTJaB7rJ4RMYzu5BvPOEk'

resp = sheet.values().update( # Добавляем данные в таблицу google sheets
    spreadsheetId=sheet_id,
    range="Лист1!A1:Z1000", # Будем заполнять таблицу от A1 до Z1000
    valueInputOption="RAW",
    body={'values': rows}).execute()

