from itertools import islice
from collections import OrderedDict
import os

import pandas as pd

import settings
import streams
import row_parser
from inspect_columns import Columns
from logs import print_elapsed_time

COLUMNS = Columns.COLUMNS
VALID_ROW_WIDTH = len(COLUMNS)


def _raw_rows(year):
    path = settings.url_local_path(year)
    return streams.yield_csv_rows(path)

def has_valid_length(_row, n=VALID_ROW_WIDTH):
    return len(_row) == n

def raw_rows(year):
    return filter(has_valid_length, _raw_rows(year))    

def as_dict(row, columns=COLUMNS):    
    return OrderedDict(zip(columns, row))

def _raw_dicts(year):
    return map(as_dict, _raw_rows(year))

def has_inn(_dict):
    return _dict['inn']
    
def raw_dicts(year):        
    return filter(has_inn, _raw_dicts(year))


assert next(raw_rows(2012))
assert next(raw_dicts(2017))
    

class Dataset:
    dtypes = row_parser.DTYPES
    colnames = row_parser.COLNAMES
    
    def __init__(self, year: int):
        self.year = year
        
    # FIXME: this is untrivial - the function accepts a dict and produces a list
    def rows(self):
        gen = raw_dicts(self.year)
        return map(row_parser.parse_row_to_list, gen)

    def dicts(self):
        gen = raw_dicts(self.year)
        return map(row_parser.parse_row_to_dict, gen)
    
# FIXME: make separate functions   
#    @staticmethod
#    def nth(gen, n):
#        return next(islice(gen, n, n + 1))
#
#    def nth_row(self, n=0):
#        return self.nth(self.rows(), n)
#
#    def nth_dict(self, n=0):
#        return  self.nth(self.dicts(), n)
    
    @property
    def path(self):
        return settings.csv_path_processed(self.year)        
    
    def to_csv(self):     
        if not os.path.exists(self.path):
            print(f"{self.year}: Saving large file to", self.path)
            streams.rows_to_csv(path = self.path,
                                stream = self.rows(),
                                cols = self.colnames)  
        else:
           print(f"{self.year}: File already exists:", self.path)

    @print_elapsed_time
    def read_dataframe(self):
        print("Reading {} dataframe...".format(self.year))
        with open(self.path, 'r', encoding='utf-8') as f:
            return pd.read_csv(f, dtype=self.dtypes)
   

#class Subset:
#    def __init__(self, year: int, inns: list):
#        self.dataset = Dataset(year)
#        self.inns = [str(x) for x in inns]
#        
#    def dicts(self):
#        for d in self.dataset.dicts():
#            inn = str(d['inn'])
#            if inn in self.inns:
#                self.inns.remove(inn)                
#                yield d
#            if not self.inns:
#                break        
#            
#    def not_found(self):
#        return "\n".join(sorted(k.inns))
#                
#    def to_csv(self, filename):
#        path = tempfile(filename)
#        if not os.path.exists(path):
#            dicts_to_csv(path = path,
#                         dict_stream = self.dicts(),
#                         column_names = self.dataset.colnames)
#            return path                                 
        
     
#if __name__ == "__main__":
#    # create model dataset 
#    stream = list(islice(RawDataset(2012).rows(), 0, 500))
#    path = tempfile('reference_dataset.txt')
#    to_csv(path, stream, cols=None)
#    # TODO: place at 
#    
#    
#    #Subset(2015, 'test1').to_csv()     
#    d = Dataset(2012)
#    a = next(Dataset(2016).dicts())
#    z = next(RawDataset(2016).get_rows())
#    import random
#    ix = [random.choice(range(100)) for _ in range(5)]
#    inns = [d.nth_dict(i)['inn'] for i in ix]
#    inns = ['2224102690', '2204026804', '2222057509', '2204026730', '2207007165']
#    s = Subset(2012, inns)
#    #gen = s.dicts()
#    #print(list(gen))
#    s.to_csv("sample5.csv")
#    
#    #df = Dataset(2016).read_dataframe()
#    #Dataset(2016).to_csv()
#    # FIXME: results in MemoryError
#    
#    doc = """6125021399
#6165111610
#5501092795
#3252005997
#2617013243
#0214005782
#6125028404
#7840322535
#2723127073
#7726311464
#6432005430
#2460222454
#2009002493
#2460205089
#7707049388
#7713591359
#4027083322
#7601000640
#7702347870
#1627005779
#6135006840
#2320102816
#5007035121
#7801499923
#2502039781
#2465102746
#7709756135
#7614005035
#2721162072
#7725027605
#7704753638
#2310119472
#7709758887
#6234028965
#6312034863
#7727541830
#2312153550
#7328063237
#1661028712
#7734046851
#4501122913
#7701897582
#1834051678
#4003034171
#2317044843
#7714175986
#7606053324
#7735128151
#7206025040
#6320002223
#2420002597
#1327000226
#6125022025
#3327823181
#1646021952
#1650161470
#4703038767
#7710884741
#7713730490
#1650206314
#2320153289
#2317010611
#5029140480
#7830002705
#2320126091
#6313036408
#2325014338
#4807013380
#7813173683
#6906011193
#4715019631
#2721167592
#5030062677
#7425756540
#2319037591
#7116145872
#5010032360
#6163082392
#1659032038
#7712094033
#5029006702
#2130001337
#7707327050
#7611020204
#7724791423
#7714005350
#1434045743
#7706273281
#7731084175
#4713008017
#6315376946
#7817312063
#7708624200
#7714046028
#6167081833
#4214018010
#3013015987
#0522016027
#2277011020
#7743816842
#7801435581
#7718532879
#5614023224
#1216015989
#7718226550
#7705620334
#7707131554
#4027077632
#5307006883
#2342016712
#7701513162
#5614054173
#2127007427
#3815011264
#2130009512
#6453010174
#2130181337
#6450079058
#7707296041
#8300005580
#7105514574
#5032172562
#0710005596
#2709001880
#3663075863
#5402480282
#3904612524
#6123015784
#7724674670
#7708320240
#4214000252
#5040066582
#6453076256
#3917016350
#7842012360
#5604009492
#7705514093
#6230004963
#5616009708
#7702334864
#5032124142
#5613001002
#3437006665
#5040058775
#2703000858
#2011002420
#7730589568
#3837049102
#5614018560
#1616016850
#6623029538
#7730052050
#7731644035
#7839395419
#7731644035
#6659190900
#2902060361
#7327016379
#7709413138
#7708710924
#7725638925
#7708304859
#7717163097
#7724736609
#7714619159
#5032178356
#7728278043
#3663029916
#7702326045
#7729355614
#7722787661
#9909391333
#9909391291
#9909391260
#7708201998
#9909001382
#9909378244
#9909439151
#9909012056"""
#
#    inns = doc.split("\n")
#    k = Subset(2016, inns)    
#    k.to_csv('179.csv')
#    
#    """Not finished:
#        
#    subsets as Excel files
#    manageable, smaller files   
#    Expert 200
#    
#"""        
#        
#        
#        
