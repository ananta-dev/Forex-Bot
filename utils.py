def get_his_data_filename(pair, granularity):
    return f"his_data/{pair}_{granularity}.pkl"

def get_instruments_data_filename():
    return "his_data/@instruments.pkl"

def get_ma_test_results_data_filename():
    return "his_data/@ma_test_res.pkl"

if __name__ == "__main__":
    print(get_his_data_filename("EUR_USD","H1"))
    print(get_instruments_data_filename())


