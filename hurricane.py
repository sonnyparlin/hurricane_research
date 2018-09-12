from bs4 import BeautifulSoup
import re
import urllib.request

with urllib.request.urlopen("http://www.aoml.noaa.gov/hrd/tcfaq/E23.html") as url:
    html = url.read()

soup = BeautifulSoup(html, features="html.parser")
table = soup.find_all("table")[1]
myfile = open('Hurricane.txt', 'w')

for tr in table.find_all("tr"):
    tds=list(tr.stripped_strings)
    
    try:
        year=tds[0]
        month=tds[1]
        state=tds[2]
        category=tds[3]
        pressure=tds[4]
        max_wind=tds[5]
        name=tds[6]
        
        # Check if category is one numberic character
        # If not, that means state had a newline which means
        # there's state data in the tds[3] variable. So 
        # now we create the state variable out of tds[2] and tds[3]. 
        # Then we have to reassign the remaining original variables 
        # accordingly: category, pressure, max_wind and name.
        check_cat = re.compile("[0-9]{1}")
        if not check_cat.match(category):
            state="{0} {1}".format(tds[2], tds[3])
            category=tds[4]
            pressure=tds[5]
            max_wind=tds[6]
            name=tds[7]
        
        pattern = re.compile("^([0-9]{4}s)")
        if pattern.match(year):
            continue
            
        pattern2 = re.compile("^([0-9])")
        if pattern2.match(year):
            
            if max_wind == "980": # Fix for flaw in data from original source
                max_wind="-----"
            
            if "None" in month or "None" in state:
                print("{0}|None".format(tds[0]))
                continue
            elif pattern.match(year):
                continue
            else:  
                state = state.rstrip()
                state = re.sub(",",";",state)
                print("{0},{1},{2},{3},{4},{5},{6}".format(year,month,state,category,pressure,max_wind,name))
                myfile.write("{0},{1},{2},{3},{4},{5},{6}\n".format(year,month,state,category,pressure,max_wind,name))
            
    except IndexError:
        pass
    
myfile.close()