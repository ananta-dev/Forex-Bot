import pandas as pd
from pandas.io.pickle import read_pickle
import utils
import instrument

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

    print(f"{i_pair.name} {one_mashort} {one_malong} trades:{df_trades.shape[0]} gain:{df_trades['GAIN'].sum():.0f}")
    return df_trades['GAIN'].sum()


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

def run():
    
    granularity = "H1"
    ma_short = [8, 16, 32, 64]
    ma_long = [32, 64, 96, 128, 256]

    pairs_to_test = ['GBP_JPY', 'EUR_USD', 'EUR_CHF']
    
    for pairname in pairs_to_test:
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
                if res > best:
                    best = res
                    b_mashort = this_mashort
                    b_malong = this_malong
        print(f"Best:{best:.0f} MA-SHORT: {b_mashort:.0f} MA-LONG: {b_malong:.0f}")
        print()


if __name__ == "__main__":
    run()


    