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
ace_data=[]

class MyPrompt(Cmd):
    prompt = 'hurricane> '
    intro = "Welcome! Type ? to list commands"
    
    __hidden_methods = ('do_EOF')    
    def get_names(self):
        return [n for n in dir(self.__class__) if n not in self.__hidden_methods]
     
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
    
    '''
    def do_average_windspeed(self, inp):
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
    '''
    
    # Number of storms per year according to http://www.stormfax.com/huryear.htm
    def do_graph_storms_per_year(self,inp):
        '''Graph the number of storms per year via stormfax data in a bar graph'''
        if len(ace_data) == 0:
            self.do_read_ace_data(inp)
        
        years,storms,hurricanes,mh_hurricanes=[],[],[],[]
        for a in ace_data:
            ye,ns,h,mh,ac=a.split(",")
            years.append(int(ye))
            storms.append(int(ns))
            hurricanes.append(int(h))
            mh_hurricanes.append(int(mh))
    
        x=years
        y=storms
                        
        # Create a trace
        stormL = go.Bar(
            x = x,
            y = y,
            name='Storms'
        )
        
        hurricanesL = go.Bar(
            x = x,
            y = hurricanes,
            name='Hurricanes'
        )
        
        mh_hurricanesL = go.Bar(
            x = x,
            y = mh_hurricanes,
            name='Major Hurricanes'
        )
        
        layout = go.Layout(title='Storms from 1850 to present',
                           barmode="stack")
                   
        fig = go.Figure(data=[mh_hurricanesL,hurricanesL,stormL], layout=layout)
        py.plot(fig, filename='Storms per year line chart')
        
            
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
                size=speeds,
                sizemode='area',
                sizeref=2.*max(speeds)/(30.**2),
                sizemin=2,
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
            text='',
            showarrow=False,
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
        
        
    def do_graph_ace(self,inp):
        '''Graph the ace index of all hurricanes from 1850 to present in a scatter plot'''
        if len(ace_data) == 0:
            self.do_read_ace_data(inp)
        
        year,ace,tx=[],[],[]    
        for a in ace_data:
            ye,ns,nh,nmh,ac=a.split(",")
            year.append(int(ye))
            ace.append(int(ac))
            tx.append("Storms {}\nHurricanes {}\nMajor Hurricanes {}\nAverage Ace Index {}".format(ns,nh,nmh,ac))
                
        x=year
        y=ace
                        
        # Create a trace
        data = go.Scatter(
            x = x,
            y = y,
            text=tx,
            mode = 'markers',
            marker = dict(
                color = '#FF0000',
                size=ace,
                sizemode='area',
                sizeref=2.*max(ace)/(100.**2),
                sizemin=4,
                line = dict(width = 2)
            ),
            name='Ace index'
        )
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
        line = slope*np.asarray(x)+intercept
        
        annotation = go.layout.Annotation(
            x=1970,
            y=90,
            text='',
            showarrow=False,
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
                           title='Accumulated Cyclone Energy from 1850 to present',
                           annotations=[annotation])
                   
        fig = go.Figure(data=[data,trace2], layout=layout)
        py.plot(fig, filename='Ace index scatter plot')
        
    
    def do_graph_category(self,inp):
        '''Graph the average hurricane category for every 25 years from 1850 to present'''
        if len(h_data) == 0:
            self.do_read_h_data(inp)
            
        year,cat,tx=[],[],[]
        flag=0
        for h in h_data:
            ye,mo,st,ct,pr,ws,nm=h.split(",")
            year.append(int(ye))
            cat.append(int(ct))
            tx.append("Hurricane {}\nYear {}\nCategory {}".format(nm,ye,ct))
        
        x=year
        y=cat
        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
        line = slope*np.asarray(x)+intercept
        
        tracer = go.Scatter(
            x=x,
            y=line,
            mode='lines',
            marker=go.scatter.Marker(color='rgb(31, 119, 180)'),
            name='Trendline'
        )
                          
        data = go.Scatter(
            x = x,
            y = y,
            text=tx,
            mode = 'markers',
            marker = dict(
                color = '#FF0000',
                size=y,
                sizemode='area',
                sizeref=2.*max(y)/(30.**2),
                sizemin=4,
                line = dict(width = 2)
            ),
            name='Category index'
        )
        
        annotation = go.layout.Annotation(
            x=1850,
            y=2,
            text='',
            showarrow=False,
            font=go.layout.annotation.Font(size=16)
        )

        layout = go.Layout(
            title='Hurricane category historical data',
            annotations=[annotation]
        )
        fig = go.Figure(data=[data,tracer], layout=layout)
        py.plot(fig, filename='Category Scatter Plot')
         
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
                
        #self.do_dump_h_data(inp)
        
        
    def do_read_ace_data(self, inp):
        '''Collect data from http://www.aoml.noaa.gov/hrd/hurdat/comparison_table.html for functions on that dataset'''
        with open('ace_data.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                year=row[0]
                num_storms=row[1]
                num_hurricanes=row[2]
                num_maj_hurricanes=row[3]
                ace=row[4]
                ace_data.append("{},{},{},{},{}".format(year,num_storms,num_hurricanes,num_maj_hurricanes,ace))
        
        #self.do_dump_ace_data(inp)

    def do_update_ace_data(self,inp):
        '''Re-scrape data from original web (stormfax) source and rebuild csv file, 
this should only be done every so often, the data doesn't change much.'''
        f = io.StringIO()
        with redirect_stdout(f):
            hurricane_scraper.scrape_and_dump_ace()
        print(f.getvalue())

    def do_dump_ace_data(self,inp):
        '''Display dump of raw data'''
        if len(ace_data) == 0:
            self.do_read_ace_data(inp)
    
        csv_reader = csv.reader(ace_data, delimiter=',')
        for row in csv_reader:
            year=row[0]
            num_storms=row[1]
            num_hurricanes=row[2]
            num_maj_hurricanes=row[3]
            ace=row[4]
            print("{},{},{},{},{}".format(year,num_storms,num_hurricanes,num_maj_hurricanes,ace))

    def do_clear_ace_data(self,inp):
        '''Clear stormfax data from memory'''
        ace_data=[]
        print(ace_data)
 
if __name__ == '__main__':
    MyPrompt().cmdloop()