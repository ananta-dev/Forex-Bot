import pandas as pd
import utils

class Instrument():
    def __init__(self, ob):
        self.name = ob['name']
        self.ins_type = ob['type']
        self.displayName = ob['displayName']
        self.pipLocation = pow(10, ob['pipLocation'])   # -4 -> 0.0001
        self.marginRate = ob['marginRate']
        
    def __repr__(self):
        return str(vars(self))

    @classmethod
    def get_instruments_df(cls):
        file_name = utils.get_instruments_data_filename()
        data = pd.read_pickle(file_name)
        return data

    @classmethod
    def get_instruments_list(cls):
        df = Instrument.get_instruments_df()
        my_list = df.to_dict(orient='records')
        return [Instrument(x) for x in my_list]


if __name__ == "__main__":
    print(Instrument.get_instruments_list())
    


