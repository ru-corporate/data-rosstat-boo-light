"""Download csv file from Rosstat web site."""

import requests
import os
import platform
from settings import url, url_local_path


URL = { 
        0: 'http://s3.eu-central-1.amazonaws.com/boo2012/data_reference.rar',    
     2012: 'http://www.gks.ru/opendata/storage/7708234640-bdboo2012/data-20181029t000000-structure-20121231t000000.csv',
     2013: 'http://www.gks.ru/opendata/storage/7708234640-bdboo2013/data-20181029t000000-structure-20131231t000000.csv',
     2014: 'http://www.gks.ru/opendata/storage/7708234640-bdboo2014/data-20181029t000000-structure-20141231t000000.csv',
     2015: 'http://www.gks.ru/opendata/storage/7708234640-bdboo2015/data-20181029t000000-structure-20151231t000000.csv',
     2016: 'http://www.gks.ru/opendata/storage/7708234640-bdboo2016/data-20181029t000000-structure-20161231t000000.csv',
     2017: 'http://www.gks.ru/opendata/storage/7708234640-bdboo2017/data-20181029t000000-structure-20171231t000000.csv',
    }


IS_WINDOWS = (platform.system() == 'Windows')

# RAR executable
if IS_WINDOWS:
    UNPACK_RAR_EXE = str(PROJECT_ROOT / 'bin' / 'unrar.exe')
else:
    UNPACK_RAR_EXE = 'unrar'
    
def _download(url: str, path: str):
    r = requests.get(url, stream=True)
    with open(path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    return path


def download(year, force=False):    
    url = URL.get(year) 
    _path = url_local_path(year)
    if os.path.exists(_path) and not force:
        print(year, "Already downloaded", _path)
    else:
        print(year, "Downloading", _url)
        _download(_url, _path)
        print(year, "Saved", _path)

        
def download_force(year: int):
            
        
        
if __name__ == "__main__":
    download(2012)
    #download(2013)
    #download(2014)
    #download(2015)
    #download(2016)
    #download(2017)