import requests
import os
import json
import pandas as pd
from datetime import datetime as dt
import matplotlib.pyplot as plt


class CryptoTool:
    base_url = 'https://api.coingecko.com/api/v3/'

    def __init__(self, api_url=base_url):
        # create directories to store data
        self.base_url = api_url
        self.cwd = os.getcwd()
        self.req_dir = self.cwd + '/data/required/'
        self.user_dir = self.cwd + '/data/user/'
        os.makedirs(self.req_dir, exist_ok=True)
        os.makedirs(self.user_dir, exist_ok=True)

        # get data for available coins and save it as a json file
        coin_list = requests.get(self.base_url + 'coins/list')
        with open(self.req_dir + 'coins_list.json', 'w') as f:
            f.write(json.dumps(coin_list.json()))

        # get data for available vs currencies and save it as a json file
        vs_currencies = requests.get(self.base_url + 'simple/supported_vs_currencies')
        with open(self.req_dir + 'supported_vs_currencies.json', 'w') as f:
            f.write(json.dumps(vs_currencies.json()))

        # create a dataframe with the coins, symbols and ids
        self.coin_df = pd.DataFrame(coin_list.json())
        self.coin_df['name'] = self.coin_df['name'].str.lower()
        self.coin_df = self.coin_df.set_index('name')

        # create a dataframe for vs_currencies
        self.vs_currencies_df = pd.DataFrame(vs_currencies.json())

    def get_coin_history(self, coin, vs, download=True): # add something so if the symbol is unique just use this coin
        _coin = coin.lower().strip()
        _vs = vs.lower().strip()
        parameters = {'vs_currency': _vs, 'days': 'max'}

        if _coin in self.coin_df.index:
            if _vs in self.vs_currencies_df.values:
                coin_id = self.coin_df.loc[_coin]['id']
                coin_data = requests.get(f'{self.base_url}/coins/{coin_id}/market_chart', params=parameters)
                if download:  # USE HELPER FUNCTION??
                    with open(self.user_dir + f'{coin_id}_{_vs}.json', 'w') as f:
                        f.write(json.dumps(coin_data.json()))
                    print(f'Data successfully downloaded to {self.user_dir}{coin_id}_{_vs}.json')
                else:
                    return coin_data.json()
            else:
                print(f"vs currency '{vs}' not recognised")

        elif _coin in self.coin_df['symbol'].values:  # if the symbol is found, suggests coins with the symbol
            print("Please enter the name of your coin! (symbols are not unique)")
            print("e.g. " + ", ".join(self.coin_df[self.coin_df['symbol'] == _coin].index))
        else:
            print(f"{coin} not recognised")


    def plot_history(self, coin, vs, key='prices', days=None):
        coin_data = self.get_coin_history(coin, vs, download=False)

        if coin_data:
            data = [x[1] for x in coin_data[key][-days:]]
            dates = [dt.fromtimestamp(x[0]/1000) for x in coin_data[key][-days:]]
            plt.plot(dates, data)
            plt.yscale("log")
            plt.title(f'{coin.title()} / {vs.upper()} ({key[:-1].title().replace("_"," ")})')
            plt.grid(which='both')
            plt.show()




if __name__ == "__main__":
    test = CryptoTool()
    # test.get_coin_history('cardano', 'usd')
    test.plot_history('cardano', 'usd', key='total_volumes')





