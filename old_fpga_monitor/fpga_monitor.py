from hardware.toptica import toptica
from hardware.fpga import fpga
from gfx import gui, graph
import winsound

colors=[(155,155,255), (255,155,155), (255,255,55), (155,255,155)]
sound=True

# function to render useful information to the screen
def render():
	gfx.cls()
	labels, cols, y = ['A','B','C','D'], [0,1,2,3], 10
	for i in range(4):
		gfx.text('%s :  %d' % (labels[i], counts[cols[i]]), 510, y, 40, colors[i])
		y+=45
	labels, cols, y = ['AB','AD','BC','CD'], [8,9,10,11], 220
	for i in range(4):
		gfx.text('%s : %d' % (labels[i], counts[cols[i]]), 510, y, 40, colors[i])
		y+=45
	
	singles_plot.draw(gfx);	coincidences_plot.draw(gfx); zoom_plot.draw(gfx); norm_plot.draw(gfx)
	gfx.text('Sound is %s (press S to switch)' % ('on' if sound else 'off'), 510, 410, 12, (255,255,255))
	gfx.update()
	
# the user pressed a key on the keyboard
def key_down(key):
	global sound
	if key==115: 
		sound=not sound
		render()
		gfx.sleep(1)
		
	if key==32: 
		singles_plot.clear()
		coincidences_plot.clear()
	
# gracefully close the program
def quit():
	fpga.kill()
	gfx.quit()

# set up the gui interface
gfx=gui('FPGA Monitor', 800, 650)
gfx.bindQuit(quit)
gfx.bindKeyPress(key_down)
singles_plot=graph((10, 10, 490, 200), 4)
coincidences_plot=graph((10, 220, 490, 200), 4)
zoom_plot=graph((10, 430, 245, 200), 1)
norm_plot=graph((10+245+10, 430, 235, 200), 4, 100)

# connect to the fpga
fpga=fpga(COM=5)
# main loop
while True:
	counts=fpga.read()
	print counts
	if sound:
		f=sum([counts[i] for i in range(4)])*0.01
		if 40<f<32760: winsound.Beep(f, 50)
		
	singles_plot.add_points(counts[0:4])
	coincidences_plot.add_points(counts[8:12])
	a=None
	try:
		a=[x/float(sum(counts[8:12])) for x in counts[8:12]]
	except:
		a=[0 for x in counts[8:12]]
		
	norm_plot.add_points(a)
	
	try:
		efficiency=counts[8]/float(counts[0]+counts[1])
	except:
		efficiency=0
	
	zoom_plot.add_points([efficiency])
	
	render()
	gfx.sleep(0)

quit()
