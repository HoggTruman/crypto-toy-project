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

    @staticmethod
    def _to_dataframe(data):
        return pd.concat([pd.DataFrame(data[k], columns=['date', k]).set_index('date') for k in data], axis=1)

    def _write(self, data, cur_1, cur_2, key=''):  # pass in a json string for data??
        with open(self.user_dir + f'{cur_1}_{cur_2}{key}.json', 'w') as f:
            f.write(data)
        print(f'Data successfully written to {self.user_dir}{cur_1}_{cur_2}{key}.json')


    def _fetch_data(self, coin, vs, download):
        parameters = {'vs_currency': vs, 'days': 'max'}
        coin_id = self.coin_df.loc[coin]['id']
        coin_data = requests.get(f'{self.base_url}/coins/{coin_id}/market_chart', params=parameters)
        if download:
            self._write(json.dumps(coin_data.json()), coin_id, vs)
        else:
            return self._to_dataframe(coin_data.json())


    def get_coin_history(self, coin, vs, download=True):
        _coin = coin.lower().strip()
        _vs = vs.lower().strip()

        if _coin in self.coin_df.index:
            if _vs in self.vs_currencies_df.values:
                return self._fetch_data(_coin, _vs, download)
            else:
                print(f"vs currency '{vs}' not recognised")
        elif _coin in self.coin_df['symbol'].values:
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


    def coin_vs_coin_history(self, coin, vs_coin, key='prices', download=True):
        coin_df = self.get_coin_history(coin, 'usd', download=False)
        coin_vs_df = self.get_coin_history(vs_coin, 'usd', download=False)

        compare_df = (coin_df[key]/coin_vs_df[key]).dropna()
        coin_id = self.coin_df.loc[coin]["id"]
        vs_coin_id = self.coin_df.loc[vs_coin]["id"]

        if download:
            self._write(compare_df.to_json(), coin_id, vs_coin_id, '_'+key)
        else:
            return compare_df



if __name__ == "__main__":
    # manual testing
    # test = CryptoTool()
    # # test.get_coin_history('cardano', 'usd')
    # # test.plot_history('cardano', 'usd', key='total_volumes')
    # test.get_coin_history('ethereum', 'usd')
    # data = test.coin_vs_coin_history('cardano', 'bitcoin', download=False)
    # print(type(data))
    pass





