import csv    
import urllib.request
from collections import OrderedDict


def update_hurdat():
    try:
        with urllib.request.urlopen("https://www.nhc.noaa.gov/data/hurdat/hurdat2-1851-2022-050423.txt") as url:
            html = url.read()
    except urllib.error.HTTPError as e:
        sys.stdout.write("Error connecting to website {}\n".format(e))
    
    myfile = open("hurdat.csv", "wb")
    myfile.write(html)
    myfile.close()

def build_ri_index():
    with open('hurdat.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        speeds=[]
        name_date_string=""
        old_name_date=""
        h={}
        i=0
        for row in csv_reader:
            i+=1
            if len(row) == 4:
                # we hit anew row, clear the data.
                name="{},{}".format(row[0].strip(),row[1].strip())
                date=row[0][4:9]
                name_date_string = "{},{}".format(name.strip(),date)
                h[name_date_string]=[]
                speeds=[]
            else:
                hour=row[1]
                speed=row[6]
                speeds.append(int(speed.strip()))
                h[name_date_string]=speeds
            
        #print(h)
        for key,value in h.items():
            if not value:
                continue
            m = max(value)
            value = value[:value.index(m)+1]
            h[key]=value
    
        for context,w_speeds in h.items():
            z=0
            b=[]
            while z < len(w_speeds):
                tmp = w_speeds[z:z+4]
                if len(tmp) == 4:
                    b.append(w_speeds[z:z+4])
                z+=1
        
            h[context]=b
        
        hurdat = open("hurdat_data.csv","w")
        for context,w_speeds in h.items():
            for arr in w_speeds:
                maxval = max(arr)
                minval = min(arr)
                #print("maxval is {} minval is {} arr is {} difference is {}".format(maxval,minval,arr,maxval-minval))
                if maxval - minval > 30:
                    hurdat.write("{}\n".format(context))
                    print(context)

        hurdat.close()
