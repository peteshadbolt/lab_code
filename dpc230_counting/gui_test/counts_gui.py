import os, time
import wx
from qy import settings
from gui_components import *

class counts_gui(wx.Frame):
    ''' A simple GUI to talk to counting systems '''
    def __init__(self, pipe):
        ''' Constructor '''
        self.pipe=pipe
        self.app = wx.App(False)
        self.build()
        self.load_defaults()

    
    def mainloop(self):
        ''' The main loop '''
        self.app.MainLoop()

    
    #def check_messages(self):
        #while self.pipe.poll():
            #message=self.hardware_pipe.recv()
            #if message[0] == 'count_rates': 
                #pass
                #counts=[]
                #for index, item in enumerate(message['count_rates'].items()):
                    #key, value = item
                    #counts.append((index, key, value))
                #filtered_counts=self.gui.browser.update_counts(counts)
                #self.gui.graph.add_counts(filtered_counts)


    def build(self):
        ''' Builds the various pieces of the GUI ''' 
        wx.Frame.__init__(self, None, title='FPGA', size=(500,100))
        self.SetBackgroundColour(wx.Colour(212, 208, 200))
        self.Bind(wx.EVT_CLOSE, self.quit)

        # Build both panels
        self.build_graph_panel()
        self.build_left_panel()
        
        # The main sizer
        self.mainsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.mainsizer.Add(self.left_panel, 0, wx.ALL|wx.EXPAND, 5)
        self.mainsizer.Add(self.graph, 1, wx.EXPAND)
        
        # Put things together
        self.SetSizerAndFit(self.mainsizer)
        self.Show()
        self.SetMinSize((800,500))
        self.SetSize((800,500))
        
    def build_left_panel(self):
        ''' Build the left panel '''

        # Prepare the panel
        self.left_panel_sizer=wx.BoxSizer(wx.HORIZONTAL)
        self.left_panel=wx.Panel(self)
        self.left_panel.SetSizer(self.left_panel_sizer)
        self.left_panel.SetMinSize((260, 100))

        # Status boxes
        status=wxbasics.output_box(self.left_panel ,border=True)
        self.left_panel_sizer.Add(status, 1, wx.EXPAND|wx.TOP, 5)

        # Graph configuration
        #graph_config_sizer=wx.BoxSizer(wx.HORIZONTAL)
        #graph_config_sizer.Add((0,0), 1)
        #self.left_panel_sizer.Add(graph_config_sizer, 0, wx.BOTTOM, 8)

        # Browser
        self.browser=wxbrowser.browser(self.left_panel)
        self.browser.bind_change(self.graph.clear)
        

    def build_graph_panel(self):
        ''' build the right panel '''
        self.graph=wxgraph.graph_panel(self)
                

    def quit(self, *args):
        ''' Close down gracefully, and then destroy the window '''
        self.save_defaults()
        self.pipe.send(('gui_quit', None))
        self.Destroy()


    def load_defaults(self):
        patterns=settings.get('realtime.browser_searches')
        #self.gui.browser.set_patterns(patterns)
        
    def save_defaults(self):
        pass
        #qy.settings.put('realtime.browser_searches', self.gui.browser.get_text_patterns())


class dummy_pipe:
    def __init__(self):
        pass

    def recv(self):
        return None, None

    def send(self, arg):
        return None


if __name__=='__main__':
    g=counts_gui(dummy_pipe())
    g.mainloop()









