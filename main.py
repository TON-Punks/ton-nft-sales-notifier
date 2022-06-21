# -*- coding: utf-8 -*-
import requests
import time
import json
from datetime import datetime
import pytz
from config import *
import schedule


def main():
    old_utime = open(f'{current_path}/LastSaleDatetime', 'r').read()
    try:
        last_utime = int(open(f'{current_path}/LastSaleDatetime', 'r').read())
        success = False
        while not success:
            try:
                response = json.loads(requests.get(
                    "https://toncenter.com/api/v2/getTransactions", params=main_params).text)
                response = response['result']
                success = True
            except:
                print('Get Request Failed')
        for transaction in response[::-1]:
            if transaction['utime'] <= last_utime:
                continue
            transaction = transaction['in_msg']
            if transaction['@type'] == 'raw.message' and transaction['message'] == '':
                address = transaction['source']
                second_params['address'] = address
                transactions = json.loads(requests.get(
                    "https://toncenter.com/api/v2/getTransactions", params=second_params).text)
                prices, timings = [], []
                isnft = False
                market = 'Unknown Marketplace'
                for i in transactions['result'][::-1]:
                    try:
                        for out in i['out_msgs']:
                            try:
                                market = marketplaces[out['destination']]
                                break
                            except:
                                pass
                    except:
                        pass
                    msg = i['in_msg']
                    time.sleep(1)
                    try:
                        nft = json.loads(
                            requests.get(f'https://tonapi.io/v1/nft/getItem?account={msg["source"]}').text)
                        if nft['collection_address'] == detect_address(COLLECTION_ADDRESS)['raw_form']:
                            data = nft['metadata']
                            name = data['name']
                            image = data['image']
                            nft_address = msg['source']
                            isnft = True
                    except:
                        if i['utime'] <= last_utime:
                            continue
                        else:
                            open(f'{current_path}/LastSaleDatetime', 'w').write(str(i['utime']))
                        price = int(msg['value'])
                        if price >= 1000000000:
                            prices += [price / (10 ** 9)]
                            timings += [str(datetime.fromtimestamp(i['utime'], tz=pytz.utc).strftime('%d.%m.%Y %H:%M:%S'))]
                if isnft:
                    print(f'New deal on {market}: {name}')
                    price = round(float(max(prices)), 3)
                    emoji = '💎'
                    floor = {'disintar': [10**20, ''],
                             'getgems': [10**20, '']}
                    try:
                        getgems_floor = json.loads(requests.post('https://api.getgems.io/graphql', json=getgems_data).text)['data']['alphaNftItemSearch']['edges'][0]['node']
                        floor['getgems'] = [round(float(getgems_floor['sale']['fullPrice']) / (10 ** 9), 3),
                                            f"https://getgems.io/collection/{detect_address(COLLECTION_ADDRESS)['bounceable']['b64url']}/{getgems_floor['address']}"]
                    except:
                        print('Get GetGems Floor Failed')
                    try:
                        disintar_floor = json.loads(requests.post('https://beta.disintar.io/api/get_entities/',
                                                                  headers=disintar['headers'],
                                                                  data=disintar['get_floor']).text)['data'][0]
                        floor['disintar'] = [round(float(disintar_floor['price']), 3),
                                             f"https://beta.disintar.io/object/{disintar_floor['address']}"]
                    except:
                        print('Get Disintar Floor Failed')
                    try:
                        floor_market = 'disintar' if floor['disintar'][0] < floor['getgems'][0] else 'getgems'
                        floor_price, floor_link = floor[floor_market]
                        floor_text = f'🔽 <b>Current <a href="{floor_link}">floor</a>:</b> {floor_price} TON'
                        if price <= floor_price * 1.1:
                            emoji = '🍣'
                    except:
                        floor_text = ''
                        print('Get Floor Failed')
                    buy_time = timings[prices.index(max(prices))]
                    try:
                        dollars = json.loads(requests.get('https://ru.ton.org/getpriceg/').text)['the-open-network']['usd']
                        dollars = str(round(float(price) * float(dollars), 2))
                        dollars_text = f'({dollars}$)'
                    except:
                        dollars_text = ''
                        print('Get Dollars Failed')
                    message_text = f'👾 <b><a href="https://explorer.tonnft.tools/nft/{nft_address}">{name}</a></b>\n\n' \
                                   f'' \
                                   f'{emoji} #Purchased for <b>{price} TON {dollars_text} on {market}</b>\n\n' \
                                   '' \
                                   f'⌚ <b>Date and time of buy:</b> {buy_time} UTC\n' \
                                   f'{floor_text}'
                    for chat in chats:
                        try:
                            bot.sendPhoto(chat, photo=image, caption=message_text, parse_mode='HTML')
                        except Exception as e:
                            print(f'Photo Send ({chat}) Failed: {e}')
                            try:
                                bot.sendMessage(chat, message_text, parse_mode='HTML', disable_web_page_preview=True)
                            except Exception as e:
                                print(f'Message Send ({chat}) Failed: {e}')
    except Exception as e:
        open(f'{current_path}/LastSaleDatetime', 'w').write(old_utime)
        print(e)


schedule.every(15).seconds.do(main)

while True:
    schedule.run_pending()
    time.sleep(1)
