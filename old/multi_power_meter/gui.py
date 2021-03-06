import winsound, os, time
import wx
import qy
import qy.graphics

from gui_components import *

class gui:
    def __init__(self, hardware_pipe, postprocessing_pipe):
        ''' constructor '''
        self.hardware_pipe=hardware_pipe
        self.postprocessing_pipe=postprocessing_pipe
        self.app = wx.App(False)
        self.gui=wxgui(self)
    
    def mainloop(self):
        self.app.MainLoop()
        
    def check_messages(self):
        while self.hardware_pipe.poll():
            message=self.hardware_pipe.recv()
            #if 'text' in message: self.gui.status_boxes[0].set_label(message['text'])
            
        while self.postprocessing_pipe.poll():
            message=self.postprocessing_pipe.recv()
            #if 'text' in message: self.gui.status_boxes[0].set_label(message['text'])
            if 'count_rates' in message: 
                self.gui.graph.add_counts(zip(range(6), map(str, range(6)), message['count_rates']))
                
    def quit(self):
        self.postprocessing_pipe.send({'quit':None})
        self.hardware_pipe.send({'quit':None})
        
        
#########################################################################################       
        
class wxgui(wx.Frame):
    def __init__(self, parent):
        self.parent=parent
        self.build()
        self.buildtimer()
        
    def buildtimer(self):
        ''' the main loop '''
        self.timer=wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.ontimer, self.timer)
        self.timer.Start(100)
        
    def ontimer(self, event):
        self.parent.check_messages()
        self.Update()
        
    def build_status_boxes(self):
        ''' build three status boxes '''
        self.status_boxes=[]
        for i in range(1):
            status=wxbasics.output_box(self.left_panel ,border=True)
            self.left_panel_sizer.Add(status, 0, wx.EXPAND|wx.BOTTOM, 5)
            self.status_boxes.append(status)
        
    def build_graph_config(self):
        ''' build the dpc config '''
        graph_config_sizer=wx.BoxSizer(wx.HORIZONTAL)
        self.log_scale=wx.CheckBox(self.left_panel, label='Log scale')
        
        #graph_config_sizer.Add(self.play_sound, 0)
        #graph_config_sizer.Add(self.hi_contrast, 0, wx.LEFT, 20)
        graph_config_sizer.Add(self.log_scale, 0, wx.LEFT, 20)
        graph_config_sizer.Add((0,0), 1)
        self.left_panel_sizer.Add(graph_config_sizer, 0, wx.BOTTOM, 8)
        
    def build_left_panel(self):
        ''' build the left panel '''
        self.left_panel_sizer=wx.BoxSizer(wx.VERTICAL)
        self.left_panel=wx.Panel(self)
        #self.build_status_boxes()
        self.build_graph_config()
        
        self.left_panel.SetSizer(self.left_panel_sizer)
        self.left_panel.SetMinSize((200, 100))
        
    def build_graph_panel(self):
        ''' build the right panel '''
        self.graph=wxgraph.graph_panel(self)
        self.log_scale.Bind(wx.EVT_CHECKBOX, self.graph.set_log_scale)
        
    def quit(self, event=None):
        ''' happens when the window is closed '''
        self.parent.quit()
        self.Destroy()
                
    def build(self):
        '''' build the gui '''
        wx.Frame.__init__(self, None, title='Power meter', size=(500,100))
        self.SetBackgroundColour(wx.Colour(212, 208, 200))
        self.Bind(wx.EVT_CLOSE, self.quit)
            
        # build both panels
        self.build_left_panel()
        self.build_graph_panel()
        
        # the main sizer
        self.mainsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.mainsizer.Add(self.left_panel, 0, wx.ALL|wx.EXPAND, 5)
        self.mainsizer.Add(self.graph, 1, wx.EXPAND)
                
        self.SetSizerAndFit(self.mainsizer)
        self.Show()
        self.SetMinSize((800,500))
        self.SetSize((800,500))
        
        
