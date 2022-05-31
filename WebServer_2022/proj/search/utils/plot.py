import io
import time
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from django.core.files.images import ImageFile


class Plot:
    
    def __init__(self, IPorCOM, start_datehour, total_hour):
        self.IPorCOM = IPorCOM
        self.start_datehour = start_datehour
        self.total_hour = int(total_hour)
        
        split_datehour = self.start_datehour.rsplit('.',1) # start_datehour = '2019.08.17.13'
        self.start_date = split_datehour[0]                # 'YYYY.MM.DD'
        self.start_UTCsec = time.mktime(time.strptime(self.start_datehour, "%Y.%m.%d.%H"))
        self.end_UTCsec = self.start_UTCsec + 3600*self.total_hour-1

        # Initialization      
        self.data_arrays = []
        self.fileOpenTimes = 0
        self.getPlotAllInfo = False 
        self.last_point_index_firstday = 0
        self.num_of_lines = -1        
        self.plot_info ={}
        self.x_points = []
        
        
    def plot_figure(self):
        result = self.get_plot_allInfo()
        
        if not result:
            return None
                
        # General setting
        figure = io.BytesIO()
        title = self.plot_info['Type']+'_'+self.IPorCOM+'('+self.start_datehour+')'
        color = ('#ff0000', '#006600', '#ff8000')
        plt.switch_backend('agg')
        fig, ax1 = plt.subplots()
        fig.patch.set_facecolor('k')
        ax1.patch.set_facecolor('k')
        plt.title(title, color='#fbdf2d')
        ax1.grid(True, linestyle='--', color='#9b6cf9', linewidth=1.1)
        for spine in ["left", "top", "right", "bottom"]:
            ax1.spines[spine].set_color('c')
               
        # 1st lable
        ax1.set_xlabel('Time(H)', color='#fbdf2d')
        ax1.set_ylabel('Temperature(\'C)', color=color[0])
        ax1.set_xlim(0, self.total_hour)
        ax1.tick_params(axis='x', labelcolor='y', colors='y')
        ax1.tick_params(axis='y', labelcolor=color[0], colors=color[0])
        
        
        if len(self.plot_info['ylable_name'])>1:
        # 2nd line
            ax2 = ax1.twinx()
#             ax2.set_ylim(0, 100)
            ax2.set_ylabel('Relative Humidity(%RH)', color=color[1])
            ax2.tick_params(axis='y', labelcolor=color[1], colors=color[1])
    
            ax2.yaxis.set_minor_locator(AutoMinorLocator())
            ax2.tick_params(which='minor', length=4, color=color[1])

        for index_data, each in  enumerate(self.plot_info['line_legend']):
            # 'line_legend': ['Temperature_PV', 'Humidty_PV']
            front_of_each = each.split('_')[0]
            if self.plot_info['ylable_name'].index(front_of_each)==0:
                ax1.plot(self.x_points, 
                         self.data_arrays[index_data], 
                         color=color[index_data], 
                         linewidth=0.8,
                         alpha=0.7)
                
            if self.plot_info['ylable_name'].index(front_of_each)==1:
                ax2.plot(self.x_points, 
                         self.data_arrays[index_data], 
                         color=color[index_data], 
                         linewidth=0.8, 
                         alpha=0.7)
               
        # Final setting
        line_legend = tuple(self.plot_info['line_legend'])
        leg = fig.legend(line_legend,loc='lower center',ncol=3, bbox_to_anchor=(0.5, -0.05))
    
        color_legend = color[:len(line_legend)]
        for index, text in enumerate(leg.get_texts()):
            text.set_color(color_legend[index])
    
        ax1.xaxis.set_minor_locator(AutoMinorLocator())
        ax1.yaxis.set_minor_locator(AutoMinorLocator())
        ax1.tick_params(axis='y', which='minor', length=4, color='tab:red', width=1.1)
        ax1.tick_params(axis='x', which='minor', length=4, color='#fbdf2d', width=1.1)
    
        
        fig.tight_layout()      
        plt.savefig(figure, format = 'png', 
                    dpi=300, facecolor='k', 
                    bbox_extra_artists=(leg,), 
                    bbox_inches='tight')
        
#         plt.savefig('test.png', dpi=300, facecolor='k', bbox_extra_artists=(leg,), bbox_inches='tight')
        
        imagename = self.IPorCOM+'_'+self.start_datehour+'_'+str(self.total_hour)
        content_file = ImageFile(figure)        
        return (imagename, content_file)    

    def get_ChartjsVariables(self):
        
        if self.getPlotAllInfo==False:
            self.get_plot_allInfo()
          
        if self.getPlotAllInfo==True and self.data_arrays:
                            
            chartjsvariables = {}
            chartjsData = []
#             chartjslabels = ''
            daysTimestamp = []
            
            # total_hour_Vs_TimeInterval => key(total hour), value(time interval of every datum in seconds)
            total_hour_Vs_TimeInterval = \
                {1:60, 2:60, 3:60, \
                4:300, 5:300, 6:300, 7:300, 8:300, 9:300, 10:300, 11:300, 12:300, 13:300, 14:300, 15:300, \
                16:600, 17:600, 18:600, 19:600, 20:600, 21:600, 22:600, 23:600, 24:600}
            chartjsDataInterval = \
                total_hour_Vs_TimeInterval[self.total_hour]//self.plot_info['Interval time']
            
            chartjsTimeInterval = self.plot_info['Interval time'] * chartjsDataInterval
            
            
            for each_lineData in self.data_arrays:
                Data = []
                firstDayData = each_lineData[:self.last_point_index_firstday:chartjsDataInterval]
                secondDayData = each_lineData[self.last_point_index_firstday::chartjsDataInterval]
                Data = firstDayData + secondDayData
                chartjsData.append(Data)           
            
            
            firstday_stamp = \
                (round(self.start_UTCsec + self.x_points[0]*3600),) if firstDayData else (0,)
            
            seconday_stamp = \
                (round(self.start_UTCsec + self.x_points[self.last_point_index_firstday]*3600),) \
                if secondDayData else (0,)
            data_start_inTimestamp = firstday_stamp + seconday_stamp 
            
            data_length = len(firstDayData)          
            for eachday_Timestamp in data_start_inTimestamp:
                daysTimestamp.extend([int(eachday_Timestamp + chartjsTimeInterval*i) for i in range(data_length)])
                data_length = len(Data) - data_length
            
            chartjsvariables['title'] = self.plot_info['Type']+'_'+self.IPorCOM+'('+self.start_datehour+')'        
            chartjsvariables['tick_max'] = int(self.end_UTCsec*1000)
            chartjsvariables['tick_min'] = int(self.start_UTCsec*1000)
            chartjsvariables['labels'] = daysTimestamp
            chartjsvariables['data'] = chartjsData
            chartjsvariables['legend'] = self.plot_info['line_legend']
            chartjsvariables['ylable_name'] = self.plot_info['ylable_name']  
            
            print(chartjsvariables)
            print(self.plot_info)        
            return chartjsvariables
        
        return None
    
    def get_plot_allInfo(self):
        
        self.getPlotAllInfo = True
        
        file_name = self.get_file_name()
        content_inline = self.open_device_file(file_name)
        if content_inline == None:
            self.fileOpenTimes=1
            file_name = self.get_file_name()
            content_inline = self.open_device_file(file_name)           
            if content_inline == None:
                return None
        
        self.get_plot_settings(content_inline[0:3])
        self.get_recording_data(content_inline[3:])
        
        self.last_point_index_firstday = len(self.x_points) if self.fileOpenTimes==0 else 0            
#         self.last_point_index_firstday = len(self.x_points)
        
        notEnoughPoints = len(self.x_points)<(3600*self.total_hour//self.plot_info['Interval time'])
        if notEnoughPoints and (self.fileOpenTimes==0):
            self.fileOpenTimes = 1
            file_name = self.get_file_name()
            content_inline = self.open_device_file(file_name)
            if content_inline:
                self.set_new_Record_start_time(content_inline[1])
                self.get_recording_data(content_inline[3:])
        return True 

    def get_file_name(self):
    # choose which file to be open
        if self.fileOpenTimes==0:
            file_name = 'Server_'+self.IPorCOM+'_'+self.start_date+'.csv'
    
        if self.fileOpenTimes==1:
            next_start_date = self.start_date[:-2]+str(int(self.start_date[-2:])+1).zfill(2)
            file_name = 'Server_'+self.IPorCOM+'_'+next_start_date+'.csv'
        return file_name  
    
    def open_device_file(self, file_name):
        file_dir = '/home/proj/web/Data/'+self.IPorCOM+'/'+file_name
        try:
            with open(file_dir, 'r') as rfile:
                content = rfile.read()
                content_inline = tuple(content.splitlines())
                return content_inline
    
        except FileNotFoundError:
                return None      
        
    def get_plot_settings(self, content_firstThreeLine):
        # content_inline[0] = 'Type,ESS,Interval Time(s),6'
        line_detail_split = content_firstThreeLine[0].split(',')
        self.plot_info['Type'] = line_detail_split[1]  # Type
        interval_time = int(line_detail_split[3])
        self.plot_info['Interval time'] = interval_time  # Interval Time(s)
     
        # content_inline[1] = 'Start Time,2020.08.13,16:57:30'
        line_detail_split = content_firstThreeLine[1].split(',', 1)
        record_datetime = line_detail_split[1]
        record_UTCsec = time.mktime(time.strptime(record_datetime, "%Y.%m.%d,%H:%M:%S"))
        self.plot_info['Record_start_time'] = (record_UTCsec,)  # Start timestamp(seconds) in float
              
        # content_inline[2] = ',Temperature_PV,Humidty_PV,---'
        line_detail_split = content_firstThreeLine[2].strip(',---').split(',')
        self.plot_info['line_legend'] = line_detail_split
        self.plot_info['ylable_name'] = sorted(
                                                set([each.split('_')[0] for each in line_detail_split]),
                                                reverse=True)
        if self.fileOpenTimes==0 or self.num_of_lines==-1: # no default input for num_of_lines
            self.num_of_lines = len(line_detail_split)
        self.data_arrays = [[] for _ in range(self.num_of_lines)]

    def set_new_Record_start_time(self, content_oneLine):
        line_detail_split = content_oneLine.split(',', 1)
        record_datetime = line_detail_split[1]
        record_UTCsec = time.mktime(time.strptime(record_datetime, "%Y.%m.%d,%H:%M:%S"))
        self.plot_info['Record_start_time'] += (record_UTCsec,)  # Start time  
                      
    def get_recording_data(self, content_rest):
        for line_detail in content_rest:            
            line_detail_split = line_detail.split(',')
            try:             
                current_UTCsec = self.plot_info['Record_start_time'][-1] \
                                +int(line_detail_split[0])*self.plot_info['Interval time']
                                
                if (current_UTCsec>=self.start_UTCsec) and (current_UTCsec<=self.end_UTCsec):
                    self.x_points.append((current_UTCsec-self.start_UTCsec)/3600)
                    for index_line, each_line in enumerate(self.data_arrays):
                        each_line.append(float(line_detail_split[index_line + 1]))
        
                if current_UTCsec>self.end_UTCsec:
                    break
            except ValueError:
                pass
            
           
       

    
    

        
if __name__ =="__main__":
    IPorCOM = '192.168.10.62'
    start_datehour = '2021.10.13.0'
    total_hour= '12'
    plot = Plot(IPorCOM, start_datehour, total_hour)
#     result = plot.get_plot_allInfo()
#     result = plot.plot_figure()
    result = plot.get_ChartjsVariables()
    print(result)
     
        
        
#===============================================================================
#         plt.savefig('hello.png', dpi=300, facecolor='k', bbox_extra_artists=(leg,), bbox_inches='tight')
#         plt.close()
#         plt.show()
#         T_H_Image.objects.create(image_name = imagename, image=content_file)
#===============================================================================
