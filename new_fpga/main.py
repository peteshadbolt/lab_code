from multiprocessing import Process, Pipe

def hardware_loop(hard_post, hard_gui):
    from hardware_server import hardware_server
    s=hardware_server(hard_post, hard_gui)
    s.mainloop()
    
def postprocessing_loop(post_hard, post_gui):
    from postprocessing_server import postprocessing_server
    s=postprocessing_server(post_hard, post_gui)
    s.mainloop()

    
def gui_loop(gui_hard, gui_post):
    from gui import gui
    s=gui(gui_hard, gui_post)
    s.mainloop()
    
    
if __name__ == '__main__':
    hard_post, post_hard = Pipe()
    hard_gui, gui_hard = Pipe()
    post_gui, gui_post = Pipe()
    
    hardware = Process(target=hardware_loop, name='hardware_server', args=(hard_post,hard_gui))
    hardware.start()
    
    postprocessing = Process(target=postprocessing_loop, name='postprocessing_server', args=(post_hard, post_gui))
    postprocessing.start()
        
    gui = Process(target=gui_loop, name='gui', args=(gui_hard, gui_post))
    gui.start()
