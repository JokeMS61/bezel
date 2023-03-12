
class Loop(object):
    
    def __init__(object):
        self.iteration_count = 0
    
    def step(self):
        self.iteration_count+= 1

class FixedStepLoop(Loop):
    
    def __init__(object):
        
        self.iteration_count = 0
        self.start_time = None
        self.last_time = 0.
    
    def start(self):
        
        self.start_time = get_time();
    
    def step(self):
        
        T = get_time()
        
    