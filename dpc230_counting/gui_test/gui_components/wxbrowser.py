import wx
import qy
import qy.graphics
import wxbasics

class browser_input(wx.Panel):
    def __init__(self, parent):
        ''' a label box with an optional border '''
        wx.Panel.__init__(self, parent, style=wx.SIMPLE_BORDER)
        self.SetBackgroundColour(wx.Colour(255,255,255))
        
        sizer=wx.BoxSizer(wx.VERTICAL)
        self.text=wx.TextCtrl(self, style=wx.NO_BORDER)
        self.text.SetFont(wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        sizer.Add(self.text, 0)
        self.SetSizerAndFit(sizer)
        
    def set_value(self, value):
        self.text.SetValue(value)
        
    def get_value(self):
        return self.text.GetValue().upper()

class browser_output(wx.Panel):
    def __init__(self, parent, colour):
        ''' a label box with an optional border '''
        wx.Panel.__init__(self, parent, style=wx.SIMPLE_BORDER)
        
        self.SetBackgroundColour(colour)
        self.SetDoubleBuffered(True)
        
        sizer=wx.BoxSizer(wx.VERTICAL)
        self.text=wx.StaticText(self, label='', style=wx.ST_NO_AUTORESIZE|wx.ALIGN_RIGHT)
        
        self.text.SetFont(wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        self.text.SetLabel('')
        sizer.Add(self.text, 1, wx.RIGHT|wx.EXPAND, 4)
        sizer.SetMinSize((150,20))
        self.SetSizerAndFit(sizer)
        
    def set_value(self, value):
        ''' set the value of the label '''
        if value==None:
            self.text.SetLabel('--')
        else:
            self.text.SetLabel(str(int(value)))

class browser_block(wx.Panel):
    def __init__(self, parent, colour):
        ''' a label box with an optional border '''
        wx.Panel.__init__(self, parent)
        self.colour=wx.Colour(*colour)
        sizer=wx.BoxSizer(wx.HORIZONTAL)
        
        self.input=browser_input(self)
        self.output=browser_output(self, self.colour)
        
        sizer.Add(self.input, 0, wx.RIGHT|wx.LEFT, 2)
        sizer.Add(self.output, 1, wx.EXPAND)
        self.SetSizerAndFit(sizer)
        self.Fit()
        
    def bind(self, function):
        self.input.text.Bind(wx.EVT_TEXT, function)
        
    def get_value(self):
        return self.input.get_value()
        
    def set_label(self, value):
        self.input.set_value(value)
        
    def set_value(self, value):
        self.output.set_value(value)
        
class browser(wx.Panel):
    def __init__(self, parent, number=16):
        ''' constructor '''
        wx.Panel.__init__(self, parent)
        self.build()
        
    def build(self):
        ''' build the widget '''
        mainsizer=wx.BoxSizer(wx.VERTICAL)
        self.blocks=[]
        for i in range(16):
            colour=qy.graphics.colors.get_pastel_rgb(i)
            colour=wx.Colour(*colour)
            block=browser_block(self, colour)
            block.bind(self.patterns_changed)
            self.blocks.append(block)
            mainsizer.Add(block, 0, wx.TOP|wx.EXPAND, border=2)
        self.SetSizerAndFit(mainsizer)
        
    def set_patterns(self, patterns):
        ''' set all of the patterns '''
        for i in range(min(len(patterns), len(self.blocks))):
            self.blocks[i].set_label(patterns[i])
        
    def get_text_patterns(self):    
        ''' get all of the patterns as text '''
        return [b.get_value() for b in self.blocks]
        
    def patterns_changed(self, event):
        ''' this happens every time the user changes the pattern selection '''
        l=self.get_text_patterns()
        if self.on_change!=None:
            self.on_change()

    def bind_change(self, function):
        self.on_change=function
        
    def update_counts(self, counts):
        ''' the postprocessing system sent us new count rates. process them, and forward the filtered counts onto the graph '''
        text_patterns=self.get_text_patterns()
        normalize = lambda x: ''.join(sorted(x.lower().strip()))
        data=[]

        for request_index, pattern in enumerate(text_patterns):
            for count_index, label, value in counts:
                if normalize(label)==normalize(pattern):
                    self.blocks[request_index].set_value(int(value))
                    data.append((request_index, label, value))


        return data

                    
        
