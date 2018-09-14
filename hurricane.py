from cmd import Cmd
import plotly.plotly as py
import plotly.graph_objs as go
from scipy import stats
import numpy as np
import csv, io
import hurricane_scraper
from contextlib import redirect_stdout
h_data=[]
sf_data=[]

class MyPrompt(Cmd):
    prompt = 'hurricane> '
    intro = "Welcome! Type ? to list commands"
    
    __hiden_methods = ('do_EOF')    
    def get_names(self):
        return [n for n in dir(self.__class__) if n not in self.__hiden_methods]
     
    def do_exit(self, inp):
        '''exit the application. Shorthand: x q Ctrl-D.'''
        print("Bye")
        return True
        
    do_EOF = do_exit
        
    def emptyline(self):
        pass
      
    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)
    
    def do_average_windspeed(self, inp):
        '''Graph average windspeed of U.S. landfall hurricanes per year from 1850 to present'''
        if len(h_data) == 0:
            self.do_read_h_data(inp)
        
        speeds=[]    
        for h in h_data:
            ye,mo,st,ct,pr,ws,nm=h.split(",")
            #if int(ye) < 1934: # option to omit data for testing purposes
            #    print(ye)
            #    continue
            if not "---" in ws:
                speeds.append(int(ws))
            
        print(sum(speeds) / len(speeds))

    def do_average_category(self, inp):
        '''Get average category of U.S. landfall hurricanes per year from 1850 to present'''
        if len(h_data) == 0:
            self.do_read_h_data(inp)
        
        cats=[]    
        for h in h_data:
            ye,mo,st,ct,pr,ws,nm=h.split(",")
            #if int(ye) < 1934: # option to omit data for testing purposes
            #    print(ye)
            #    continue
            if not "---" in ws:
                cats.append(int(ct))
            
        print(sum(cats) / len(cats))
    
    # Number of storms per year according to http://www.stormfax.com/huryear.htm
    def do_graph_storms_per_year(self,inp):
        '''Graph the number of storms per year via stormfax data in a bar graph'''
        if len(sf_data) == 0:
            self.do_read_sf_data(inp)
        
        years,storms,hurricanes,mh_hurricanes=[],[],[],[]
        for sf in sf_data:
            ye,ns,h,mh=sf.split(",")
            years.append(int(ye))
            storms.append(int(ns))
            hurricanes.append(int(h))
            mh_hurricanes.append(int(mh))
    
        x=years
        y=storms
                        
        # Create a trace
        stormL = go.Scatter(
            x = x,
            y = y,
            name='Storms per Year'
        )
        
        hurricanesL = go.Scatter(
            x = x,
            y = hurricanes,
            name='Hurricanes per Year'
        )
        
        mh_hurricanesL = go.Scatter(
            x = x,
            y = mh_hurricanes,
            name='Major hurricanes per Year'
        )
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
        line = slope*np.asarray(x)+intercept
        
        annotation = go.layout.Annotation(
            x=1980,
            y=14,
            text='Trend line',
            showarrow=True,
            font=go.layout.annotation.Font(size=16)
        )
        
        trace2 = go.Scatter(
            x=x,
            y=line,
            mode='lines',
            marker=go.scatter.Marker(color='rgb(255, 0, 0)'),
            name='Trendline'
        )

        layout = go.Layout(title='Storms from 1850 to present (stormfax data)',
                           annotations=[annotation])
                   
        fig = go.Figure(data=[stormL,hurricanesL,mh_hurricanesL,trace2], layout=layout)
        py.plot(fig, filename='Storms per year bar chart (stormfax data)')
        
            
    def do_graph_hurricanes_per_year(self,inp):
        '''Graph the number of U.S. landfall hurricanes per year from 1850 to present in a bar graph'''
        if len(h_data) == 0:
            self.do_read_h_data(inp)
        
        years,hurricanes=[],[]    
        for h in h_data:
            ye,mo,st,ct,pr,ws,nm=h.split(",")
            #if int(ye) < 1934: # option to omit data for testing purposes
            #    print(ye)
            #    continue
            years.append(int(ye))
                
        from collections import Counter
        num_h_per_year = Counter(years)
        (years,hurricanes) = zip(*num_h_per_year.items()) #Convert dict to two arrays python 3
        x=years
        y=hurricanes
                        
        # Create a trace
        data = go.Bar(
            x = x,
            y = y,
            name='Hurricanes per Year'
        )
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
        line = slope*np.asarray(x)+intercept
        
        annotation = go.layout.Annotation(
            x=1974,
            y=2.5,
            text='Trend line',
            showarrow=True,
            font=go.layout.annotation.Font(size=16)
        )
        
        trace2 = go.Scatter(
            x=x,
            y=line,
            mode='lines',
            marker=go.scatter.Marker(color='rgb(255, 0, 0)'),
            name='Trendline'
        )

        layout = go.Layout(title='Hurricanes from 1850 to present',
                           annotations=[annotation])
                   
        fig = go.Figure(data=[data,trace2], layout=layout)
        py.plot(fig, filename='Hurricanes per year bar chart')
            
    def do_graph_windspeed(self,inp):
        '''Graph the windspeeds of all hurricanes from 1850 to present in a scatter plot'''
        if len(h_data) == 0:
            self.do_read_h_data(inp)
        
        speeds,hurricanes=[],[]    
        for h in h_data:
            ye,mo,st,ct,pr,ws,nm=h.split(",")
            if not "---" in ws:
                speeds.append(int(ws))
                hurricanes.append(int(ye))
                
        x=hurricanes
        y=speeds
                        
        # Create a trace
        data = go.Scatter(
            x = x,
            y = y,
            mode = 'markers',
            marker = dict(
                color = '#FF0000',
                line = dict(width = 1)
            ),
            name='Max Wind'
        )
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
        line = slope*np.asarray(x)+intercept
        
        annotation = go.layout.Annotation(
            x=1970,
            y=90,
            text='Minimal Upward Trend',
            showarrow=True,
            font=go.layout.annotation.Font(size=16)
        )
        
        trace2 = go.Scatter(
            x=x,
            y=line,
            mode='lines',
            marker=go.scatter.Marker(color='rgb(31, 119, 180)'),
            name='Trendline'
        )

        layout = go.Layout(xaxis=dict(ticks='', showticklabels=True, zeroline=False),
                           yaxis=dict(ticks='', showticklabels=True, zeroline=False),
                           showlegend=True, hovermode='closest', 
                           title='Wind speeds of all hurricanes from 1850 to present',
                           annotations=[annotation])
                   
        fig = go.Figure(data=[data,trace2], layout=layout)
        py.plot(fig, filename='Wind speed scatter plot')
    
    def do_graph_category(self,inp):
        '''Graph the average hurricane category for every 25 years from 1850 to present'''
        if len(h_data) == 0:
            self.do_read_h_data(inp)
            
        c1,c2,c3,c4,c5,c6,c7=[],[],[],[],[],[],[]
        all_ranges,ydata=[],[]
        flag=0
        for h in h_data:
            ye,mo,st,ct,pr,ws,nm=h.split(",")
            if int(ye) > 1850 and int(ye) < 1875:
                c1.append(int(ct))
            elif int(ye) > 1876 and int(ye) < 1899:
                c2.append(int(ct))
            elif int(ye) > 1900 and int(ye) < 1924:
                c3.append(int(ct))
            elif int(ye) > 1925 and int(ye) < 1949:
                c4.append(int(ct))
            elif int(ye) > 1950 and int(ye) < 1974:
                c5.append(int(ct))
            elif int(ye) > 1975 and int(ye) < 1999:
                c6.append(int(ct))
            elif int(ye) > 2000 and int(ye) < 2024:   
                c7.append(int(ct))
                
        all_ranges=[c1,c2,c3,c4,c5,c6,c7]
        labels=["1850-1875","1876-1899","1900-1924","1925-1949","1950-1999","2000-2024"]
        labels_linear=[1850,1876,1900,1925,1950,1975,2000]
        for range in all_ranges:
            ydata.append(sum(range)/len(range))
        
        x=labels_linear
        y=ydata
        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
        line = slope*np.asarray(x)+intercept
        
        tracer = go.Scatter(
            x=x,
            y=line,
            mode='lines',
            marker=go.scatter.Marker(color='rgb(255, 0, 0)'),
            name='Trendline'
        )
                          
        data = go.Bar(
            x=x,
            y=y
        )
        
        annotation = go.layout.Annotation(
            x=1850,
            y=2,
            text='Minimal Upward Trend 1.8 -> 2.0 over 150+ years',
            showarrow=True,
            font=go.layout.annotation.Font(size=16)
        )

        layout = go.Layout(
            title='Average Hurricane category Every 25 Years',
            annotations=[annotation]
        )
        fig = go.Figure(data=[data,tracer], layout=layout)
        py.plot(fig, filename='Category bar chart')
         
    def do_dump_h_data(self,inp):
        '''Display dump of raw data'''
        if len(h_data) == 0:
            self.do_read_h_data(inp)
        
        csv_reader = csv.reader(h_data, delimiter=',')
        for row in csv_reader:
            year=row[0]
            month=row[1]
            state_data=row[2]
            category=row[3]
            pressure=row[4]
            max_wind=row[5]
            name=row[6]
            print("{},{},{},{},{},{},{}".format(year,month,state_data,category,pressure,max_wind,name))

    def do_update_h_data(self,inp):
        '''Re-scrape data from original web (noaa.gov) source and rebuild csv file, 
this should only be done every so often, the data doesn't change much.'''
        f = io.StringIO()
        with redirect_stdout(f):
            hurricane_scraper.scrape_and_dump()
        print(f.getvalue())
        
    def do_clear_h_data(self,inp):
        '''Clear data from memory'''
        h_data=[]
        print(h_data)
        
    def do_read_h_data(self, inp):
        '''Collect data for all other functions, this should run first'''
        with open('Hurricane.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                year=row[0]
                month=row[1]
                state_data=row[2]
                category=row[3]
                pressure=row[4]
                max_wind=row[5]
                name=row[6]
                h_data.append("{},{},{},{},{},{},{}".format(year,month,state_data,category,pressure,max_wind,name))
    
    def do_read_sf_data(self, inp):
        '''Collect data from stormfax_list.csv for functions on that dataset'''
        with open('stormfax_list.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                year=row[0]
                num_storms=row[1]
                num_hurricanes=row[2]
                num_maj_hurricanes=row[3]
                sf_data.append("{},{},{},{}".format(year,num_storms,num_hurricanes,num_maj_hurricanes))

    def do_update_sf_data(self,inp):
        '''Re-scrape data from original web (stormfax) source and rebuild csv file, 
this should only be done every so often, the data doesn't change much.'''
        f = io.StringIO()
        with redirect_stdout(f):
            hurricane_scraper.scrape_and_dump_sf()
        print(f.getvalue())
    
    def do_dump_sf_data(self,inp):
        '''Display dump of raw data'''
        if len(h_data) == 0:
            self.do_read_sf_data(inp)
        
        csv_reader = csv.reader(sf_data, delimiter=',')
        for row in csv_reader:
            year=row[0]
            num_storms=row[1]
            num_hurricanes=row[2]
            num_maj_hurricanes=row[3]
            print("{},{},{},{}".format(year,num_storms,num_hurricanes,num_maj_hurricanes))

    def do_clear_sf_data(self,inp):
        '''Clear stormfax data from memory'''
        sf_data=[]
        print(sf_data)
 
if __name__ == '__main__':
    MyPrompt().cmdloop()