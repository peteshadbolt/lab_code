import wx
import qy
import wxbasics
from datetime import datetime

class scan_dialog(wx.Dialog):
	def __init__(self, parent, callback):
		''' a dialog to control the delays '''
		self.callback=callback
		self.build(parent)		
		
	def show_hide(self, event=None):
		if not self.dont_move.IsChecked():
			f='Scan taken at %H:%M:%S on %A %d/%m/%Y'
		else:
			f='Sample taken at %H:%M:%S on %A %d/%m/%Y'
		s=datetime.strftime(datetime.now(), f)
		self.scan_label.SetValue(s)
		
	def start(self, event):
		self.save_defaults()
		
		output={}
		output['scan_start_position']=self.start_position.get_value()
		output['scan_stop_position']=self.stop_position.get_value()
		output['scan_npoints']=self.npoints.get_value()
		output['scan_integration_time']=self.integration_time.get_value()
		output['scan_motor_controller']=self.motor_controller.GetValue()
		output['scan_label']=self.scan_label.GetValue()
		output['scan_dont_move']=self.dont_move.GetValue()
		output['scan_nloops']=self.nloops.get_value()
		output['scan_close_shutter']=self.close_shutter.GetValue()
		self.callback(output)
		
		self.Destroy()
		
	def cancel(self, event):
		self.Destroy()
		
	def save_defaults(self):
		qy.settings.put('scan_start_position', self.start_position.get_value())
		qy.settings.put('scan_stop_position', self.stop_position.get_value())
		qy.settings.put('scan_nloops', self.nloops.get_value())
		qy.settings.put('scan_npoints', self.npoints.get_value())
		qy.settings.put('scan_integration_time', self.integration_time.get_value())
		qy.settings.put('scan_motor_controller', self.motor_controller.GetValue())
		qy.settings.put('scan_dont_move', int(self.dont_move.GetValue()))
		qy.settings.put('scan_close_shutter', int(self.close_shutter.GetValue()))
		
	def build(self, parent):
		wx.Dialog.__init__(self, parent, title='Scan or Sample')
		self.mainsizer=wx.BoxSizer(wx.VERTICAL)
		
		self.npoints=wxbasics.input_output_pair(self)
		self.npoints.set_label('Number of points:')
		self.npoints.configure(int, (0,10000), int(qy.settings.get('scan_npoints')))
		self.mainsizer.Add(self.npoints, 0, wx.EXPAND|wx.ALL, 5)
		
		self.nloops=wxbasics.input_output_pair(self)
		self.nloops.set_label('Number of loops:')
		self.nloops.configure(int, (0,10000), int(qy.settings.get('scan_nloops')))
		self.mainsizer.Add(self.nloops, 0, wx.EXPAND|wx.ALL, 5)
		
		self.integration_time=wxbasics.input_output_pair(self)
		self.integration_time.set_label('Integration time (s) :')
		self.integration_time.configure(int, (1,10000), int(qy.settings.get('scan_integration_time')))
		self.mainsizer.Add(self.integration_time, 0, wx.EXPAND|wx.ALL, 5)
		
		self.close_shutter=wx.CheckBox(self, label='Close shutter at end of scan')
		self.close_shutter.SetValue(int(qy.settings.get('scan_close_shutter')))
		self.mainsizer.Add((0,5), 0)
		self.mainsizer.Add(self.close_shutter, 0, wx.EXPAND|wx.ALL, 5)
		self.mainsizer.Add((0,5), 0)
		
		self.dont_move=wx.CheckBox(self, label='Sample counts without moving')
		self.dont_move.SetValue(int(qy.settings.get('scan_dont_move')))
		self.dont_move.Bind(wx.EVT_CHECKBOX, self.show_hide)
		self.mainsizer.Add((0,5), 0)
		self.mainsizer.Add(self.dont_move, 0, wx.EXPAND|wx.ALL, 5)
		self.mainsizer.Add((0,5), 0)
		
		self.start_position=wxbasics.input_output_pair(self)
		self.start_position.set_label('Start position (mm) :')
		self.start_position.configure(float, (0,50), qy.settings.get('scan_start_position'))
		self.mainsizer.Add(self.start_position, 0, wx.EXPAND|wx.ALL, 5)
		
		self.stop_position=wxbasics.input_output_pair(self)
		self.stop_position.set_label('Stop position (mm) :')
		self.stop_position.configure(float, (0,50), qy.settings.get('scan_stop_position'))
		self.mainsizer.Add(self.stop_position, 0, wx.EXPAND|wx.ALL, 5)
		
		q=wx.BoxSizer(wx.HORIZONTAL)
		l=wx.StaticText(self, label='Motor Controller:')
		q.Add(l, 1, wx.EXPAND)
		self.motor_controller=wx.SpinCtrl(self, style=wx.SIMPLE_BORDER, size=(60, 24))
		self.motor_controller.SetRange(1, int(qy.settings.get('motors_count')))
		self.motor_controller.SetValue(int(qy.settings.get('scan_motor_controller')))
		q.Add((0,0), 1, wx.EXPAND)
		q.Add(self.motor_controller, 0, wx.EXPAND)
		self.mainsizer.Add(q, 0, wx.EXPAND|wx.ALL, 5)
		
		self.scan_label=wx.TextCtrl(self, style=wx.SIMPLE_BORDER|wx.TE_MULTILINE)
		self.scan_label.SetBackgroundColour(wx.Colour(255,255,225))
		self.mainsizer.Add(self.scan_label, 1, wx.EXPAND|wx.ALL, 5)
		
		self.time_display=wxbasics.output_box(self, border=True)
		self.mainsizer.Add(self.time_display, 0, wx.EXPAND|wx.ALL, 5)
		
		bsizer=wx.BoxSizer(wx.HORIZONTAL)
		self.start_button=wx.Button(self, label='Start')
		self.start_button.Bind(wx.EVT_BUTTON, self.start)
		bsizer.Add(self.start_button, 0, wx.EXPAND|wx.RIGHT, 5)
		
		self.cancel_button=wx.Button(self, label='Cancel')
		self.cancel_button.Bind(wx.EVT_BUTTON, self.cancel)
		bsizer.Add(self.cancel_button, 0, wx.EXPAND)
		self.mainsizer.Add(bsizer, 0, wx.EXPAND|wx.ALL, 5)
				
		self.SetSizerAndFit(self.mainsizer)
		self.SetMinSize((400,500))
		self.SetSize((300,500))
		self.show_hide()
		self.build_timer()
		
	def build_timer(self):
		''' the main loop '''
		self.timer=wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.ontimer, self.timer)
		self.timer.Start(100)
		
	def tell_estimated_time(self):
		nloops=int(self.nloops.get_value())
		npoints=int(self.npoints.get_value())
		integration_time=int(self.integration_time.get_value())
		s='Estimated duration: %.1f minutes' % (nloops*npoints*integration_time/60.)
		self.time_display.set_label(s)
		
	def ontimer(self, event):
		self.tell_estimated_time()
		self.Update()
	
	
