import os
import pathlib

import telepot
from dotenv import load_dotenv
from address import *

load_dotenv()

TONCENTER_API = os.getenv('TONCENTER_API')
BOT_TOKEN = os.getenv('BOT_TOKEN')
ROYALTY_ADDRESS = detect_address(os.getenv('ROYALTY_ADDRESS'))['bounceable']['b64url']
COLLECTION_ADDRESS = os.getenv('COLLECTION_ADDRESS')
chats = list(map(int, os.getenv('CHATS').split(';')))

bot = telepot.Bot(BOT_TOKEN)

current_path = pathlib.Path(__file__).parent.resolve()

disintar = {
    'headers': {
        'cookie': 'csrftoken=vO44viQbEDlbcKiLz56aaE8tLmjzc5XtVqUTZo6zgItxRNehF7VRGlCVdQR3dul9',
        'x-csrftoken': 'vO44viQbEDlbcKiLz56aaE8tLmjzc5XtVqUTZo6zgItxRNehF7VRGlCVdQR3dul9',
        'referer': 'https://beta.disintar.io/object/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'},
    'get_floor': {'entity_name': 'Collection',
                  'order_by': '["creation_date"]',
                  'filter_by': '[{"name":"address","value":' +
                               detect_address(COLLECTION_ADDRESS)['bounceable']['b64url'] + '}]',
                  'limit': 'null',
                  'group_by': 'null',
                  'page': '0', 'request_time': 'undefined'}
}

getgems_query = "query nftSearch($count: Int!, $cursor: String, $query: String, $sort: String) {\n  alphaNftItemSearch(first: $count, after: $cursor, query: $query, sort: $sort) {\n    edges {\n      node {\n        ...nftPreview\n        __typename\n      }\n      cursor\n      __typename\n    }\n    info {\n      hasNextPage\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment nftPreview on NftItem {\n  name\n  previewImage: content {\n    ... on NftContentImage {\n      image {\n        sized(width: 500, height: 500)\n        __typename\n      }\n      __typename\n    }\n    ... on NftContentLottie {\n      lottie\n      fallbackImage: image {\n        sized(width: 500, height: 500)\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  address\n  collection {\n    name\n    address\n    __typename\n  }\n  sale {\n    ... on NftSaleFixPrice {\n      fullPrice\n      __typename\n    }\n    __typename\n  }\n  __typename\n}"

getgems_data = {'operationName': 'nftSearch',
                'query': getgems_query,
                'variables': {
                    'count': 1,
                    'query': '{"$and":[{"collectionAddress":"' + detect_address(COLLECTION_ADDRESS)['bounceable']['b64url'] + '"}]}',
                    'sort': '[{"isOnSale":{"order":"desc"}},{"price":{"order":"asc"}},{"index":{"order":"asc"}}]'
                }}

main_params = {'address': ROYALTY_ADDRESS, 'limit': '500', 'to_lt': '0',
               'archival': 'false', 'api_key': TONCENTER_API}

second_params = {'limit': '15', 'to_lt': '0', 'archival': 'false',
                 'api_key': TONCENTER_API}

marketplaces = {'EQDrLq-X6jKZNHAScgghh0h1iog3StK71zn8dcmrOj8jPWRA': 'Disintar',
                'EQCjk1hh952vWaE9bRguFkAhDAL5jj3xj9p0uPWrFBq_GEMS': 'GetGems'}
