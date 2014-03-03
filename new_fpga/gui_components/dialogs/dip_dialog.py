from Tkinter import *
import tkFileDialog as tkFD
from datetime import datetime
import qy

class dip_dialog:
	''' ask the user to design a scan '''
	def __init__(self, parent):
		''' constructor. we are given the current delay file path '''
		self.tk_root=Toplevel(parent)
		self.tk_root.title('Scan or sample')
		self.tk_root.resizable(0,0)
		self.tk_root.wm_iconbitmap('icon.ico')
		self.output=None
		self.build()
		self.load_defaults()
		self.update()
		
	def load_defaults(self):
		''' load the default dip qy.settings '''
		self.dip_start_position.set(qy.settings.lookup('dip_start_position'))
		self.dip_stop_position.set(qy.settings.lookup('dip_stop_position'))
		self.dip_npoints.set(qy.settings.lookup('dip_npoints'))
		self.dip_nloops.set(qy.settings.lookup('dip_nloops'))
		self.dip_integration_time.set(qy.settings.lookup('dip_integration_time'))
		self.dip_motor_controller.set(qy.settings.lookup('dip_motor_controller'))
		self.dip_dont_move.set(int(qy.settings.lookup('dip_dont_move')))
		self.dip_close_shutter.set(int(qy.settings.lookup('dip_close_shutter')))
		self.default_label()
		
	def default_label(self):
		self.dip_label.delete(1.0, END)
		if not self.dip_dont_move.get():
			f='Scan taken at %H:%M:%S on %A %d/%m/%Y'
		else:
			f='Sample taken at %H:%M:%S on %A %d/%m/%Y'
		s=datetime.strftime(datetime.now(), f)
		self.dip_label.insert(END, s)
	
	def save_defaults(self):
		''' save the dip qy.settings '''
		qy.settings.write('dip_start_position', self.dip_start_position.get())
		qy.settings.write('dip_stop_position', self.dip_stop_position.get())
		qy.settings.write('dip_npoints', self.dip_npoints.get())
		qy.settings.write('dip_nloops', self.dip_nloops.get())
		qy.settings.write('dip_integration_time', self.dip_integration_time.get())
		qy.settings.write('dip_motor_controller', self.dip_motor_controller.get())
		qy.settings.write('dip_dont_move', int(self.dip_dont_move.get()))
		qy.settings.write('dip_close_shutter', int(self.dip_close_shutter.get()))
		
	def start(self):
		''' start the dip '''
		try:
			output={}
			output['dip_start_position']=float(self.dip_start_position.get())
			output['dip_stop_position']=float(self.dip_stop_position.get())
			output['dip_npoints']=int(self.dip_npoints.get())
			output['dip_integration_time']=int(self.dip_integration_time.get())
			output['dip_motor_controller']=int(self.dip_motor_controller.get())
			output['dip_label']=self.dip_label.get(1.0, END)
			output['dip_dont_move']=self.dip_dont_move.get()
			output['dip_nloops']=int(self.dip_nloops.get())
			output['dip_close_shutter']=self.dip_close_shutter.get()
		except ValueError:
			self.tk_root.destroy()
			return
		
		self.output=output
		self.save_defaults()
		self.tk_root.destroy()

		
	def update(self):
		''' just figure out the experiment duration '''
		try:
			nloops=int(self.dip_nloops.get())
			npoints=int(self.dip_npoints.get())
			integration_time=int(self.dip_integration_time.get())
			s='Estimated duration: %.1f minutes' % (nloops*npoints*integration_time/60.)
			self.summary.set(s)
		except ValueError:
			pass
			
		# now change the label colors
		color='#999999' if self.dip_dont_move.get() else '#000000'
		self.start_label.configure(fg=color)
		self.end_label.configure(fg=color)
		self.mc_label.configure(fg=color)
		
		color='#cccccc' if self.dip_dont_move.get() else '#ffffdd'
		self.start_entry.configure(bg=color)
		self.end_entry.configure(bg=color)
		#self.mc_entry.configure(bg=color)
		
		self.tk_root.after(100, self.update)
		
	def build(self):
		''' build all of the GUI elements '''
		
		q=Frame(self.tk_root); q.pack(expand=True, fill=X, padx=5, pady=5)
		l=Label(q,text='Number of of points:'); l.pack(side=LEFT)
		self.dip_npoints=StringVar()
		e=Entry(q, textvar=self.dip_npoints, width=10, bg='#ffffdd'); e.pack(side=RIGHT)
		
		q=Frame(self.tk_root); q.pack(expand=True, fill=X, padx=5, pady=5)
		l=Label(q,text='Integration time:'); l.pack(side=LEFT)
		self.dip_integration_time=StringVar()
		e=Entry(q, textvar=self.dip_integration_time, width=10, bg='#ffffdd'); e.pack(side=RIGHT)
		
		q=Frame(self.tk_root); q.pack(expand=True, fill=X, padx=5, pady=5)
		l=Label(q,text='Number of loops:'); l.pack(side=LEFT)
		self.dip_nloops=StringVar()
		e=Entry(q, textvar=self.dip_nloops, width=10, bg='#ffffdd'); e.pack(side=RIGHT)
		
		self.dip_close_shutter=BooleanVar()
		q=Frame(self.tk_root); q.pack(expand=True, fill=X, padx=5, pady=5)
		l=Checkbutton(q,text='Close laser shutter at end of scan',var=self.dip_close_shutter); l.pack(side=LEFT)
		
		self.dip_dont_move=BooleanVar()
		q=Frame(self.tk_root); q.pack(expand=True, fill=X, padx=5, pady=5)
		l=Checkbutton(q,text='Sample counts without moving',var=self.dip_dont_move, command=self.default_label); l.pack(side=LEFT)
			
		q=Frame(self.tk_root); q.pack(expand=True, fill=X, padx=5, pady=5)
		self.start_label=Label(q,text='Start position (mm):'); self.start_label.pack(side=LEFT)
		self.dip_start_position=StringVar()
		self.start_entry=Entry(q, textvar=self.dip_start_position, width=10, bg='#ffffdd'); self.start_entry.pack(side=RIGHT)
		
		q=Frame(self.tk_root); q.pack(expand=True, fill=X, padx=5, pady=5)
		self.end_label=Label(q,text='End position (mm):'); self.end_label.pack(side=LEFT)
		self.dip_stop_position=StringVar()
		self.end_entry=Entry(q, textvar=self.dip_stop_position, width=10, bg='#ffffdd'); self.end_entry.pack(side=RIGHT)
				
		q=Frame(self.tk_root); q.pack(expand=True, fill=X, padx=5, pady=5)
		self.mc_label=Label(q,text='Motor controller:'); self.mc_label.pack(side=LEFT)
		
		self.dip_motor_controller=StringVar()
		options=map(str, range(1, 1+int(qy.settings.lookup('motors_count'))))
		self.mc_entry=OptionMenu(q, self.dip_motor_controller, *options); self.mc_entry.pack(side=RIGHT)
		
		#self.dip_mc=StringVar()
		#self.mc_entry=Entry(q, textvar=self.dip_mc, width=10, bg='#ffffdd'); self.mc_entry.pack(side=RIGHT)
		
		q=Frame(self.tk_root); q.pack(expand=True, fill=X, padx=5, pady=10)
		self.dip_label=Text(q, width=50, height=5, bg='#ffffdd'); self.dip_label.pack()
		
		q=Frame(self.tk_root); q.pack(expand=True, fill=X, padx=5, pady=5)
		self.summary=StringVar()
		self.summary.set('--')
		l=Label(q, textvar=self.summary, bg='#ffffff', relief=GROOVE)
		l.pack(side=LEFT, expand=True, fill=BOTH, ipadx=5)
		
		q=Frame(self.tk_root); q.pack(expand=True, fill=X, padx=5, pady=5)
		b=Button(q, text='Start', command=self.start, width=10); b.pack(side=RIGHT)
		b=Button(q, text='Cancel', command=self.tk_root.destroy, width=10); b.pack(side=RIGHT, padx=5)