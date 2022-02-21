import setup
import os


"""get_latest() tests"""
setup.get_latest()

# Test the necessary directories can be found
def test_dir_req():
    assert os.path.isdir(os.getcwd()+'/data/required/')

def test_dir_user():
    assert os.path.isdir(os.getcwd()+'/data/user')


# Test the setup files can be found
def test_file_coins_list():
    assert os.path.isfile(os.getcwd()+'/data/required/coins_list.json')

def test_file_supported_vs_currencies():
    assert os.path.isfile(os.getcwd()+'/data/required/coins_list.json')


"""create_coin_df() tests"""
coin_df = setup.create_coin_df()

def test_bitcoin():
    assert coin_df.loc['bitcoin']['symbol'] == 'btc'






