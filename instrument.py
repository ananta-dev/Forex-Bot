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

    '''
    dict to access instruments by pair name
    instrument_dict = 
    {
        "EUR_USD" : Instrument(),
        "EUR_GBP" : Instrument(),
        "..."     : Instrument()
    }
    '''
    
    @classmethod
    def get_instruments_dict(cls):
        # Implementing this:
        # ins_list = cls.get_instruments_list()
        # new_dict = {}
        # for ins in ins_list:
        #     new_dict[ins.name] = ins
        # return new_dict
        # .... but in a more elegant manner:
        
        inst_list = cls.get_instruments_list()
        keys_list = [inst.name for inst in inst_list]
        return { k:v for (k,v) in zip(keys_list, inst_list)}

        # isn't this the same?
        # return dict(zip(inst_list,keys_list))
        
    @classmethod
    def get_instrument_by_name(cls, pairname):
        d = cls.get_instruments_dict()
        if pairname in d:
            return(d[pairname])
        else:
            return None

            
if __name__ == "__main__":
    #print(Instrument.get_instruments_list())
    #print(Instrument.get_instruments_dict())
    #for k,v in Instrument.get_instruments_dict().items():
    #    print(k,v)   
    print(Instrument.get_instrument_by_name("EUR_USD"))
    


