from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re

def simple_get(url):
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
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    print(e)

def build_year_str(raw_str):
    return raw_str[0:4]

def build_month_str(raw_str):
    month=raw_str[5:9]
    mo=re.sub("[\t\s]","",month)
    mo=re.sub("Sp-O","Sep",mo)
    mo=re.sub("Jl-A","Jul",mo)
    return mo
    
def build_state_str(raw_str):
    state=raw_str[9:15]
    st=re.sub("[\t\*\,\&\#\s+\;0-9a-z]","",state)
    st=re.sub("LA","AL",st)
    st=st[0:2]
    return st
    
def collect_data(raw_str):
    cat=raw_str[9:]
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
    
    return cat,name,pressure,max_winds
    
def tokenize_and_collect(data):
    myList = data.splitlines()
    
    myfile = open('Hurricane.txt', 'w')        
    
    for item_string in myList:
        pattern = re.compile("^([0-9]{4})")
        if pattern.match(item_string):
            item=re.sub("[\*]"," ",item_string)
            year=build_year_str(item)
            month=build_month_str(item)
            if (month == '-No'):
                continue
            state=build_state_str(item)
            cat,name,pressure,max_winds=collect_data(item)
            
            myfile.write("{0},{1},{2},{3},{4},{5},{6}\n".format(year,month,state,cat,pressure,max_winds,name))
            print(year,month,state,cat,pressure,max_winds,name)
        
    myfile.close()

raw_html = simple_get('http://www.aoml.noaa.gov/hrd/hurdat/All_U.S._Hurricanes-aug2011.html')
tokenize_and_collect((raw_html))