# Crypto Toy Project

## Description

A "toy" crypto project which makes use of the CoinGecko API to obtain coin data and do various things with it. In practice there will be better tools such as pycoingecko but the point of this was more to gain experience with areas of interest.

These areas include:  
* API calls  
* Handling data with pandas  
* Writing tests  
* General Git and GitHub workflow  

## Getting Started

### Additional Python Libraries

NEED TO CREATE A REQUIREMENTS.TXT FILE 


### Usage


```
from main import CryptoTool
ct = CryptoTool()
```

### Data Layout
Data is arranged into the following directories:
* Required data: `./data/required/`
* Additional data you request `./data/user/`


## Methods
### Coin History
Obtains the full coin history for the requested coin-vs pair. Gives some suggestions if a symbol is provided instead of id
```
ct.get_coin_history(coin, vs, download=True)
```

- **Input**: 
  - **coin**: 
    - id of the desired coin (_e.g. bitcoin, ethereum, ..._)
  - **vs**: 
    - currency to compare it to (_e.g. usd, btc, ..._)
  - **download** (_optional_):     
    - if `True`, downloads the data to `./data/user/{coin}_{vs}.json` and returns `None`
    - if `False`, returns a Pandas DataFrame containing the data
    - default: `True`

  
### Plot History
Plots a graph of the history of a coin. 
```
ct.plot_history(coin, vs, key='prices', days=None):
```

- **Input**: 
  - **coin**: 
    - id of the desired coin (_e.g. bitcoin, ethereum, ..._)
  - **vs**: 
    - currency to compare it to (_e.g. usd, btc, ..._)
  - **key** (_optional_):     
    - what data to plot (`'prices'`, `'market_caps'` or `'total_volumes'`)
    - default: `'prices'`
  - **days** (_optional_):
    - integer of number of days of data to be plotted
    - default: `None` (_plots entire history_)


### Coin vs Coin History
Obtains the full history for the requested coin/vs_coin pair

e.g. `coin = 'bitcoin'` and `vs_coin = 'ethereum'` will give price data for BTC/ETH 
```
ct.coin_vs_coin_history(coin, vs_coin, key='prices', download=True)
```

- **Input**: 
  - **coin**: 
    - id of the desired coin (_e.g. bitcoin, ethereum, ..._)
  - **vs_coin**: 
    - coin to compare it to (_e.g. bitcoin, ethereum)
  - **key** (_optional_):     
    - what data to plot (`'prices'`, `'market_caps'` or `'total_volumes'`)
    - default: `'prices'`
  - **download** (_optional_):     
    - if `True`, downloads the data to `./data/user/{coin}_{vs}_{key}.json` and returns `None`
    - if `False`, returns a Pandas Series containing the data
    - default: `True`
   




