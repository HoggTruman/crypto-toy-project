import main

import pytest
import os
import shutil

"""
ENSURE TO CLEAR ANY FILES CREATED BY A TEST IMMEDIATELY SO THAT THE DIRECTORY IS CLEAR FOR SUBSEQUENT TESTS.
"""

# Clear any data from previous tests
shutil.rmtree(os.getcwd()+'/data', ignore_errors=True)


# Create an instance of the class for testing purposes
test_tool = main.CryptoTool()


"""__init__() tests"""
@pytest.mark.init
class TestInit:
    def test_dir_req(self):
        assert os.path.isdir(os.getcwd() + '/data/required/')

    def test_dir_user(self):
        assert os.path.isdir(os.getcwd() + '/data/user')

    # Test the setup files can be found
    def test_file_coins_list(self):
        assert os.path.isfile(os.getcwd() + '/data/required/coins_list.json')

    def test_file_supported_vs_currencies(self):
        assert os.path.isfile(os.getcwd() + '/data/required/coins_list.json')

    # Test coins_df is setup correctly
    def test_bitcoin(self):
        assert test_tool.coin_df.loc['bitcoin']['symbol'] == 'btc'


"""get_coin_history() tests"""
@pytest.mark.get_coin_history
class TestGetCoinHistory:
    # !Test with bad coin name!#
    def test_MADEUPCOIN_usd(self, capsys):
        coin = 'MADEUPCOIN'
        vs = 'usd'
        test_tool.get_coin_history(coin, vs)
        captured = capsys.readouterr()
        assert captured.out == f"{coin} not recognised\n"

    def test_MADEUPCOIN_usd_not_created(self):
        assert not os.listdir(os.getcwd() + '/data/user')

    # !Test with bad vs_currency!#
    def test_bitcoin_MADEUPVS(self, capsys):
        coin = 'bitcoin'
        vs = 'MADEUPVS'
        test_tool.get_coin_history(coin, vs)
        captured = capsys.readouterr()
        assert captured.out == f"vs currency '{vs}' not recognised\n"

    def test_bitcoin_MADEUPVS_not_created(self):
        assert not os.listdir(os.getcwd() + '/data/user')

    # !Test with valid input!#
    def test_bitcoin_usd(self):
        coin = 'bitcoin'
        vs = 'usd'
        file_path = os.getcwd() + '/data/user/bitcoin_usd.json'
        test_tool.get_coin_history(coin, vs)
        assert os.path.isfile(file_path)
        os.remove(file_path)

    # !Test with valid but messy coin input!#
    def test_bitcoin_usd_messy_coin_input(self):
        coin = 'BITCOIN         '
        vs = 'usd'
        file_path = os.getcwd() + '/data/user/bitcoin_usd.json'
        test_tool.get_coin_history(coin, vs)
        assert os.path.isfile(file_path)
        os.remove(file_path)

    # !Test with valid but messy vs input!#
    def test_bitcoin_usd_messy_coin_input(self):
        coin = 'bitcoin'
        vs = 'uSD        '
        file_path = os.getcwd() + '/data/user/bitcoin_usd.json'
        test_tool.get_coin_history(coin, vs)
        assert os.path.isfile(file_path)
        os.remove(file_path)

    # !Test with symbol instead of coin name!#
    def test_btc_usd(self, capsys):
        coin = 'btc'
        vs = 'usd'
        test_tool.get_coin_history(coin, vs)
        obtained = capsys.readouterr().out
        expected = "Please enter the name of your coin! (symbols are not unique)\ne.g. bitcoin\n"
        assert obtained == expected

    def test_ada_usd(self, capsys):
        coin = 'ada'
        vs = 'usd'
        test_tool.get_coin_history(coin, vs)
        obtained = capsys.readouterr().out
        expected = "Please enter the name of your coin! (symbols are not unique)\ne.g. binance-peg cardano, cardano\n"
        assert obtained == expected

    def test_luna_usd(self, capsys):
        coin = 'luna'
        vs = 'usd'
        test_tool.get_coin_history(coin, vs)
        obtained = capsys.readouterr().out
        expected = "Please enter the name of your coin! (symbols are not unique)\ne.g. luna (wormhole), terra, wrapped terra\n"
        assert obtained == expected

    def test_no_download(self):
        coin = 'bitcoin'
        vs = 'usd'
        data = test_tool.get_coin_history(coin, vs, download=False)
        assert list(data.keys()) == ["prices", "market_caps", "total_volumes"]


@pytest.mark.coin_vs_coin_history
class TestCoinVsCoinHistory:
    def test_bitcoin_cardano(self):
        coin = 'bitcoin'
        vs_coin = 'cardano'
        data = test_tool.coin_vs_coin_history(coin, vs_coin)
        file_path = os.getcwd() + '/data/user/bitcoin_cardano_prices.json'
        assert os.path.isfile(file_path)

    def test_bitcoin_ethereum_market_caps(self):
        coin = 'bitcoin'
        vs_coin = 'ethereum'
        data = test_tool.coin_vs_coin_history(coin, vs_coin, key='market_caps')
        file_path = os.getcwd() + '/data/user/bitcoin_ethereum_market_caps.json'
        assert os.path.isfile(file_path)

    def test_no_download(self):  # tests the first value is correct, would be better to test something more concrete
        coin = 'bitcoin'
        vs_coin = 'ethereum'
        data = test_tool.coin_vs_coin_history(coin, vs_coin, download=False)
        assert round(data.loc[1438905600000], 8) == round(98.3567052632, 8)

    def test_bad_key(self):
        coin = 'bitcoin'
        vs_coin = 'polkadot'
        key = 'INVALID_KEY'
        file_path = os.getcwd() + '/data/user/bitcoin_polkadot_INVALID_KEY.json'
        correct_error = False
        try:
            data = test_tool.coin_vs_coin_history(coin, vs_coin, key)
        except KeyError:
            correct_error = True
            # we expect a key error as there is no 'INVALID_KEY' section of the data for bitcoin or polkadot
            pass

        assert not os.path.isfile(file_path) and correct_error







