import pygame, sys
from pygame.locals import *
from math import floor

class gui:
	def __init__(self, caption, width, height):
		self.quitFunction=quit
		self.keyPressFunction=None
		self.screen=None
		pygame.init()
		self.width, self.height=width, height
		self.screen = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption(caption)

	def quit(self):
		pygame.quit()
		sys.exit(0)
		
	def bindQuit(self, function):
		self.quitFunction=function
	
	def bindKeyPress(self, function):
		self.keyPressFunction=function

	def sleep(self, n):
		for i in range(n/10):
			self.events()
			pygame.display.update()
			pygame.time.delay(10)
	
	def update(self):
		self.events()
		pygame.display.update()
	
	def cls(self):
		pygame.draw.rect(self.screen, (0,0,0), (0,0,self.width,self.height))
		
	def events(self):
		for event in pygame.event.get():
			if event.type == QUIT: self.quitFunction()
			if event.type == KEYDOWN: 
				if self.keyPressFunction:
					self.keyPressFunction(event.key)
		
	def text(self, txt, x, y, s=8, c1=(255,255,255), c2=None):
		font = pygame.font.SysFont('Consolas', s, False)
		text = font.render(txt, True, c1)
		r = text.get_rect()
		r.x,r.y=x,y
		self.screen.blit(text, r)
		
	def save(self):
		pygame.image.save(self.screen, 'screenshot.png')
		
colors=[(155,155,255), (255,155,155), (255,255,55), (155,255,155)]

class graph:
	def __init__(self, rect, nchan, h=250):
		self.channels=[]
		self.rect=rect
		self.history_size=h

		for i in range(nchan): self.new_channel()
		
	def clear(self):
		for i in range(len(self.channels)):
			self.channels[i]=[0]*self.history_size
		
	def new_channel(self):
		self.channels.append([0]*self.history_size)
		
	def add_points(self, points):
		for i in range(len(points)):
			self.channels[i].append(points[i])
			self.channels[i].pop(0)
		
	def draw(self, gui):
		target=gui.screen
		pygame.draw.rect(target, (20,20,20), self.rect)
		
		fx=self.rect[2]/float(self.history_size)
		maxcounts=max([max(channel) for channel in self.channels])
				
		try:
			fy=self.rect[3]/float(maxcounts)
		except ZeroDivisionError:
			fy=self.rect[3]
			
		# grid
		if maxcounts<200:
			for i in range(int(floor(maxcounts/10))):
				y=int(self.rect[1]+self.rect[3]-i*10*fy)
				pygame.draw.line(target, (30,30,30), (self.rect[0],y), (self.rect[0]+self.rect[2], y))
		
		for channel, color in zip(self.channels, colors):
			x1, y1 = self.rect[0], self.rect[1]+self.rect[3]-channel[0]*fy
			for point in channel:
				x2, y2 = x1+fx, self.rect[1]+self.rect[3]-point*fy
				pygame.draw.aaline(target, color, (int(x1),int(y1)), (int(x2),int(y2)))
				x1, y1 = x2, y2		
				
		if abs(int(maxcounts)-maxcounts)<0.0000001:
			gui.text('%d' % maxcounts, self.rect[0]+5, self.rect[1]+5, 10)
		else:
			gui.text('%d %%' % (maxcounts*100), self.rect[0]+5, self.rect[1]+5, 10)