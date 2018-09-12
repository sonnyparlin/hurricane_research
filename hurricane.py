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
        pattern = re.compile("^([0-9]{4}s)")
        if pattern.match(tds[0]):
            continue
            
        pattern2 = re.compile("^([0-9])")
        if pattern2.match(tds[0]):
            
            if "None" in tds[1] or "None" in tds[2]:
                print("{0}|None".format(tds[0]))
                continue
            elif pattern.match(tds[0]):
                continue
            else:  
                tds[2] = re.sub(",",";",tds[2])
                print("{0},{1},{2},{3},{4},{5},{6}".format(tds[0],tds[1],tds[2],tds[3],tds[4],tds[5],tds[6]))
                myfile.write("{0},{1},{2},{3},{4},{5},{6}\n".format(tds[0],tds[1],tds[2],tds[3],tds[4],tds[5],tds[6]))
            
    except IndexError:
        pass
    
myfile.close()