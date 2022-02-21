from pycoingecko import CoinGeckoAPI
import json
import os
import pandas as pd
import requests


# def get_latest():
#     cg = CoinGeckoAPI()
#
#     # create directories to store data
#     cwd = os.getcwd()
#     req_dir = '/data/required/'
#     os.makedirs(cwd+req_dir, exist_ok=True)
#     os.makedirs(cwd+'/data/user', exist_ok=True)
#
#     # get data for available coins and save it as a json file
#     coin_list = cg.get_coins_list()
#     with open(cwd + req_dir + 'coins_list.json', 'w') as f:
#         f.write(json.dumps(coin_list))
#
#     # get data for available vs currencies and save it as a json file
#     vs_currencies = cg.get_supported_vs_currencies()
#     with open(cwd + req_dir + 'supported_vs_currencies.json', 'w') as f:
#         f.write(json.dumps(vs_currencies))

def get_latest():  # maybe just create a class and use this as the init instead
    base = 'https://api.coingecko.com/api/v3'

    # create directories to store data
    cwd = os.getcwd()
    req_dir = cwd + '/data/required'
    user_dir = cwd + '/data/user'
    os.makedirs(req_dir, exist_ok=True)
    os.makedirs(user_dir, exist_ok=True)

    # get data for available coins and save it as a json file
    coin_list = requests.get(base+'/coins/list')
    with open(req_dir + '/coins_list.json', 'w') as f:
        f.write(json.dumps(coin_list.json()))

    # get data for available vs currencies and save it as a json file
    vs_currencies = requests.get(base+'/simple/supported_vs_currencies')
    with open(req_dir + '/supported_vs_currencies.json', 'w') as f:
        f.write(json.dumps(vs_currencies.json()))

def create_coin_df():  # combine into get latest
    data = json.load(open('./data/required/coins_list.json'))
    coin_df = pd.DataFrame(data)
    coin_df['name'] = coin_df['name'].str.lower()
    coin_df = coin_df.set_index('name')
    return coin_df



if __name__ == "__main__":
    # # get_latest()
    # coin_df = create_coin_df()
    # print(coin_df)
    # print(coin_df[coin_df['symbol'] == 'btc']['id'])
    pass

