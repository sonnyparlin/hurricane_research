from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)
    
    
def split_data(data):
    myList = data.splitlines()
    
    myfile = open('Hurricane.txt', 'w')        
    
    for item_string in myList:
        pattern = re.compile("^([0-9]{4})")
        if pattern.match(item_string):
            item=re.sub("[\*]"," ",item_string)
            year=item[0:4]
            month=item[5:9]
            mo=re.sub("[\t\s]","",month)
            mo=re.sub("Sp-O","Sep",mo)
            mo=re.sub("Jl-A","Jul",mo)
            if (mo == '-No'):
                continue
            state=item[9:15]
            st=re.sub("[\t\*\,\&\#\s+\;0-9a-z]","",state)
            st=re.sub("LA","AL",st)
            st=st[0:2]
            cat=item[9:]
            cat = re.sub(r"\t","_",cat).strip()
            tokens = cat.split("_")
            str_list = filter(None, tokens)
            cat = str_list[-4].strip()
            cat = re.sub("[\D]","",cat)
            if cat == "":
                cat="TS"
            name = str_list[-1]
            name = re.sub("[-\"\s]","",name)
            pressure = str_list[-3]
            max_winds = str_list[-2]
            if len(pressure) == 1:
                pressure = max_winds
                max_winds = '-----'    
            pressure = re.sub("[-]","",pressure)
            max_winds = re.sub("[-]","",max_winds)
            
            myfile.write("{0},{1},{2},{3},{4},{5},{6}\n".format(year, mo, st,cat,pressure,max_winds,name))
            #print(year, mo, st,cat,pressure,max_winds,name)
        
    myfile.close()

raw_html = simple_get('http://www.aoml.noaa.gov/hrd/hurdat/All_U.S._Hurricanes-aug2011.html')
split_data((raw_html))