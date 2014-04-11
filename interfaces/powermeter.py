import time, sys
import numpy as np
from qy.hardware.powermeter import powermeter
from qy.gui import coincidence_counting, wxbrowser 
from qy.formats import ctx
import qy.util
from multiprocessing import Process, Pipe
import wx


class gui_head(coincidence_counting.gui_head):
    ''' A simple GUI for the DPC230 '''
    def __init__(self, pipe=None):
        ''' Constructor. Inherits from coincidence_counting '''
        coincidence_counting.gui_head.__init__(self, pipe)

    def populate_left_panel(self):
        ''' Build the left panel '''
        # Status box
        self.status=wx.StaticText(self.left_panel, label='Powermeter', style=wx.ST_NO_AUTORESIZE)
        self.status.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD))
        self.left_panel_sizer.Add(self.status, 0, wx.EXPAND|wx.BOTTOM, 5)

        # Button
        self.log_button=wx.Button(self.left_panel, label='Log data now')
        self.log_button.Bind(wx.EVT_BUTTON, self.log_data_now)
        self.left_panel_sizer.Add(self.log_button, 0, wx.EXPAND|wx.BOTTOM, 5)

        # Browser
        self.browser=wxbrowser.browser(self.left_panel)
        self.left_panel_sizer.Add(self.browser, 0, wx.EXPAND|wx.ALL)

    def log_data_now(self, event):
        self.pipe.send(['log_now', 'awd'])

class gui(coincidence_counting.gui):
    ''' A Multithreaded handler for the DPC230 GUI '''
    def __init__(self):
        ''' Constructor. Inherits from coincidence_counting '''

        # Start up the GUI process and build the communication network
        self.pipe, their_pipe = Pipe()
        self.gui = Process(target=gui_head, name='gui_head', args=(their_pipe,))
        self.gui.start()




if __name__=='__main__':

    def handle_data(data):
        ''' Handles data from the counting system '''
        # Extract pertinent information
        key, value=data
        if key=='count_rates':
            interface.send('count_rates', value['count_rates'])

    def check_gui():
        ''' Check the state of the gui '''
        for key, value in interface.collect():
            if key=='gui_quit':
                sys.exit(0)
            elif key=='log_now':
                data_file.write('powers', total.tolist())
                print 'wrote ', total


    def dpc_callback(message):
        ''' Handles messages from the DPC230 '''
        interface.send('status', message)

    # The GUI
    interface=gui()

    # The meter
    powermeter=powermeter()

    # Output file
    data_file=ctx('data/%s.ctx' % qy.util.timestamp())
    data_file.write_metadata({'scan_label':'Looking at bright light'})
    total=np.zeros(6)
    print data_file

    while True:
        total=np.zeros(6)
        for i in range(10):
            total += np.array(powermeter.read())

        data=dict(zip('abcdefg', total))
        interface.send('count_rates', data)
        check_gui()

    interface.kill()

