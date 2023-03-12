

class GameClock(object):
    
    """Manages time in a game."""
    
    def __init__(self, game_ticks_per_second=100):
        
        """Create a Game Clock object.
        
        game_ticks_per_second -- The number of 'AI' frames a second.
        
        """
            
        self.game_ticks_per_second = float(game_ticks_per_second)
        self.game_tick = 1. / self.game_ticks_per_second        
        self.speed = 1.        
        self.started = False        
        
        
    def start(self):
        
        """Starts the Game Clock. Must be called once."""
        
        self.time = 0.
        self.virtual_time = 0.
        self.game_time = 0.
        self.game_frame_count = 0
        self.real_time_passed = 0.
        
        self.real_time = self.get_real_time()
        self.started = True
        
        
    def get_real_time(self):
        
        """Returns the real time, as reported by the system clock.
        This function should be implemented in a derived class!"""
        
        raise NotImplementedError, "'get_real_time' must be supplied by the derived class."
        
        
    def update(self):
        
        """Advances time, must be called once per frame. Returns a list of game frame times."""
        
        assert self.started, "You must call 'start' before using a GameClock."
        
        real_time_now = self.get_real_time()
        
        self.real_time_passed = real_time_now - self.real_time
        self.real_time = real_time_now
        
        self.time += self.real_time_passed
        self.virtual_time+= self.real_time_passed * self.speed
        
        while self.game_time + self.game_tick < self.virtual_time:
            
            yield (self.game_frame_count, self.game_time)
            self.game_frame_count += 1
            self.game_time = self.game_frame_count * self.game_tick            
        
        self.between_frame = ( self.virtual_time - self.game_time ) / self.game_tick
    
    
    
if __name__ == "__main__":
    
    import time
    
    class TestGameClock(GameClock):
        
        def get_real_time(self):
            return time.clock()
            
    t = TestGameClock(20)
    t.start()
    
    while t.virtual_time < 2.:
        
        for (frame_count, game_time) in t.update():
            
            print "Game frame #%i, %2.2f" % (frame_count, game_time)
            
        print "\t%2.2f%% between game frame"%(t.between_frame*100.)
        time.sleep(.01)
    
