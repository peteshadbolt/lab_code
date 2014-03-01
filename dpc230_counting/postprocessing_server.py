from time import sleep 

class postprocessing_server:
    def __init__(self, pipe ):
        self.pipe=pipe

    def mainloop(self):
        print 'Postprocessor is sleeping.'
        while True:
            sleep(2)

