from cmd import Cmd
import plotly.plotly as py
import plotly.graph_objs as go
from scipy import stats
import csv

h_data=[]

class MyPrompt(Cmd):
    prompt = 'pb> '
    intro = "Welcome! Type ? to list commands"
 
    def do_exit(self, inp):
        '''exit the application. Shorthand: x q Ctrl-D.'''
        print("Bye")
        return True
      
    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)
            
    def do_windspeed_by_year(self,inp):
        '''Graph the windspeeds of all hurricanes from 1850 to present in a scatter plot'''
        if len(h_data) == 0:
            self.do_read_data(inp)
        
        speeds,hurricanes=[],[]    
        for h in h_data:
            ye,mo,st,ct,pr,ws,nm=h.split(",")
            if not "---" in ws:
                speeds.append(int(ws))
                hurricanes.append(int(ye))
                        
        # Create a trace
        data = go.Scatter(
            x = hurricanes,
            y = speeds,
            mode = 'markers',
            marker = dict(
                color = '#FF0000',
                line = dict(width = 1)
            )
        )

        layout = go.Layout(xaxis=dict(ticks='', showticklabels=True, zeroline=False),
                           yaxis=dict(ticks='', showticklabels=True, zeroline=False),
                           showlegend=True, hovermode='closest', title='Wind speeds of all hurricanes from 1850 to present')
                   
        fig = go.Figure(data=[data], layout=layout)
        py.plot(fig, filename='basic-scatter')
    
    def do_category_per_qc(self,inp):
        '''Graph the average hurricane category for every 25 years from 1850 to present'''
        if len(h_data) == 0:
            self.do_read_data(inp)
            
        c1,c2,c3,c4,c5,c6=[],[],[],[],[],[]
        all_ranges,data=[],[]
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
            elif int(ye) > 1950 and int(ye) < 1999:
                c5.append(int(ct))
            elif int(ye) > 2000 and int(ye) < 2024:
                c6.append(int(ct))
                
        all_ranges=[c1,c2,c3,c4,c5,c6]
        labels=["1850-1875","1876-1899","1900-1924","1925-1949","1950-1999","2000-2024"]
        for range in all_ranges:
            data.append(sum(range)/len(range))
                          
        data = [go.Bar(
            x=labels,
            y=data
        )]

        layout = go.Layout(
            title='Average Hurricane category Every 25 Years',
        )
        fig = go.Figure(data=data, layout=layout)
        py.plot(fig, filename='basic-bar')
         
    def do_dump_data(self,inp):
        '''Display dump of raw data'''
        if len(h_data) == 0:
            self.do_read_data(inp)
        
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