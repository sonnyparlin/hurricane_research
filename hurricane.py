from cmd import Cmd
import plotly.plotly as py
import plotly.graph_objs as go
from scipy import stats
import numpy as np
import csv, io
from hurricane_scraper import scrape_and_dump
from contextlib import redirect_stdout
h_data=[]

class MyPrompt(Cmd):
    prompt = 'hurricane> '
    intro = "Welcome! Type ? to list commands"
 
    def do_exit(self, inp):
        '''exit the application. Shorthand: x q Ctrl-D.'''
        print("Bye")
        return True
      
    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)
            
    def do_graph_windspeed(self,inp):
        '''Graph the windspeeds of all hurricanes from 1850 to present in a scatter plot'''
        if len(h_data) == 0:
            self.do_read_data(inp)
        
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
        py.plot(fig, filename='basic-scatter')
    
    def do_graph_category(self,inp):
        '''Graph the average hurricane category for every 25 years from 1850 to present'''
        if len(h_data) == 0:
            self.do_read_data(inp)
            
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
        py.plot(fig, filename='basic-bar')
         
    def do_dump_data(self,inp):
        '''Display dump of raw data'''
        if len(h_data) == 0:
            self.do_read_data(inp)
        
        print(h_data)

    def do_update_data(self,inp):
        '''Re-scrape data from original web source and rebuild csv file, 
this should only be done every so often, the data doesn't change much.'''
        f = io.StringIO()
        with redirect_stdout(f):
            scrape_and_dump()
        print(f.getvalue())
        
    def do_clear_data(self,inp):
        '''Clear data from memory'''
        h_data=[]
        print(h_data)
        
    def do_read_data(self, inp):
        '''Collect data for all other functions, this should run first'''
        with open('Hurricane.txt') as csv_file:
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
 
if __name__ == '__main__':
    MyPrompt().cmdloop()