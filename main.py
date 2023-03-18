import requests
import gspread
import time

sa = gspread.service_account(filename='serv_name.json')
sh = sa.open('Test')
wks = sh.worksheet('Class Data')


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


def get_url(page):
    return f'https://www.dextools.io/shared/analytics/pairs?limit=200&interval=24h&page={page}&chain=ether'


while True:
    time.sleep(30)
    objects = []
    page = 1
    r = requests.get(get_url(page), headers=headers)
    antifreeze = 10000

    while 'data' in r.json() and antifreeze > 0:
        antifreeze -= 1
        page += 1
        if r.status_code == 200:
            json_data = r.json()
            for obj in json_data['data']:
                objects.append([
                    f"{obj['pair']['symbol']}/{obj['pair']['symbolRef']}",
                    obj['price'],
                    f"https://www.dextools.io/app/en/ether/pair-explorer/{obj['_id']['pair']}",
                    obj['_id']['token']
                ])
        else:
            print('Не удалось получить данные. Код ошибки:', r.status_code)
        r = requests.get(get_url(page), headers=headers)

    wks.update('A2', objects)
    print('Loading...')

