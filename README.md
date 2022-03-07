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

* pandas
* matplotlib
* requests


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
    - if `False`, returns a pandas dataframe containing the data

  
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
    - plots entire history by default
   




