import pandas as pd
from pandas.io.pickle import read_pickle
import utils
import instrument
from ma_result import MAResult

def is_trade(row):
    if row.DIFF >=0 and row.DIFF_PREV < 0:
        return 1
    if row.DIFF <=0 and row.DIFF_PREV > 0:
        return -1
    return 0

def get_ma_col(ma):
    return f"MA_{ma}"

def evaluate_pair(i_pair, one_mashort, one_malong, price_data):
    price_data['DIFF'] = price_data[get_ma_col(one_mashort)]-price_data[get_ma_col(one_malong)]
    price_data['DIFF_PREV'] = price_data.DIFF.shift(1)
    price_data['IS_TRADE'] = price_data.apply(is_trade, axis='columns')
    
    df_trades = price_data[price_data.IS_TRADE!=0].copy()
    df_trades['DELTA'] = (df_trades.mid_c.diff() / i_pair.pipLocation).shift(-1)
    df_trades['GAIN'] = df_trades['DELTA'] * df_trades['IS_TRADE']

    # print(f"{i_pair.name} {one_mashort} {one_malong} trades:{df_trades.shape[0]} gain:{df_trades['GAIN'].sum():.0f}")
    
    this_result = MAResult(
        df_trades = df_trades,
        pairname = i_pair.name,
        params={'one_mashort' : one_mashort, 'one_malong' : one_malong}
    )

    return this_result


def get_price_data(pairname, granularity):
    df = read_pickle(utils.get_his_data_filename(pairname, granularity))
    non_cols = ['time', 'volume']
    mod_cols = [x for x in df.columns if x not in non_cols]
    df[mod_cols] = df[mod_cols].apply(pd.to_numeric)
    return df

def process_data(ma_short, ma_long, price_data):
    ma_set = set(ma_short + ma_long)
    for ma in ma_set:
        price_data[get_ma_col(ma)] = price_data.mid_c.rolling(window=ma).mean()
    return(price_data)

def process_results(results):
    results_list = [r.result_ob() for r in results]
    results_df = pd.DataFrame.from_dict(results_list)

    results_df.to_pickle(utils.get_ma_test_results_data_filename())
    print(results_df.shape, results_df.num_trades.sum())
    
    # print("Printing Results info()")
    # print(results_df.info())
    
    # print("Printing Results head()")
    # print(results_df.head())

def get_test_pairs(currencies_string):
    currencies_list = currencies_string.split(',')
    existing_pairs = instrument.Instrument.get_instruments_dict().keys()
    test_pairs = []

    for curr1 in currencies_list:
        for curr2 in currencies_list:
            if (curr1 != curr2):
                this_pair = f"{curr1}_{curr2}"
                if this_pair in existing_pairs:
                    test_pairs.append(this_pair)
                
    return test_pairs
                

def run():
    
    granularity = "H1"
    ma_short = [4, 8, 16, 24, 32, 64]
    ma_long = [8, 16, 32, 64, 96, 128, 256]

    results = []

    currencies = "GBP,EUR,USD,CAD,JPY,NZD,CHF"
    pairs_to_test = get_test_pairs(currencies)
    
    for pairname in pairs_to_test:
        print("running...", pairname)
        i_pair = instrument.Instrument.get_instruments_dict()[pairname]
        price_data = get_price_data(pairname,granularity)
        price_data = process_data(ma_short, ma_long, price_data)
    
        best = -float('inf')
        b_mashort = 0
        b_malong = 0

        for this_malong in ma_long:
            for this_mashort in ma_short:
                if this_mashort >= this_malong:
                    continue
                #### Evaluate the performance of the pair
                res = evaluate_pair(i_pair, this_mashort, this_malong, price_data.copy())
                results.append(res)
                
                # if res > best:
                #     best = res
                #     b_mashort = this_mashort
                #     b_malong = this_malong
        
        # print(f"Best:{best:.0f} MA-SHORT: {b_mashort:.0f} MA-LONG: {b_malong:.0f}")
        # print()
    process_results(results)

if __name__ == "__main__":
    run()


    