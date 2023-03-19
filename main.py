import requests
import gspread
import time
import logging

sa = gspread.service_account(filename='serv_name.json')
sh = sa.open('Test')
wks = sh.worksheet('Class Data')
logging.basicConfig(filename='logs.log', level=logging.ERROR)

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


def get_url(page):
    return f'https://www.dextools.io/shared/analytics/pairs?limit=200&interval=24h&page={page}&chain=ether'


while True:
    time.sleep(30)
    objects = []
    page = 1
    r = requests.get(get_url(page), headers=headers)
    antifreeze = 10000

    if r.status_code != 200:
        logging.error(f'Response code is {r.status_code}')
        break
    while 'data' in r.json() and antifreeze > 0:
        antifreeze -= 1
        page += 1
        json_data = r.json()
        for obj in json_data['data']:
            objects.append([
                f"{obj['pair']['symbol']}/{obj['pair']['symbolRef']}",
                obj['price'],
                f"https://www.dextools.io/app/en/ether/pair-explorer/{obj['_id']['pair']}",
                obj['_id']['token']
            ])
        r = requests.get(get_url(page), headers=headers)

    wks.update('A2', objects)
    print('Loading...')

