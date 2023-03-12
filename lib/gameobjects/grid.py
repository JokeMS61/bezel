class Wrap:
    
    """Constants that define how Grids handle out of range coordinate."""
    
    ( none,
     repeat,
     clamp ) = range(3)


class Grid(object):
    
    def __init__( self,  node_factory,
                         width,
                         height,
                         x_wrap = Wrap.none,
                         y_wrap = Wrap.none ):
        
        """Create a grid object.
        
        node_factory -- Callable that takes the x and y coordinate of the node
        and returns a node object. x_wrap and y_wrap parameters should be
        one of (Wrap.none, Wrap.repeat, Wrap.clamp).
        
        width -- Width of the grid.
        height -- Height of the grid.
        x_wrap -- How to handle out of range x coordinates
        y_wrap -- How to handle out of range y coordinates        
        
        """
        
        self.node_factory = node_factory
        self.width = width
        self.height = height
        
        nodes = []
        
        for y in xrange(height):
            nodes.append( [node_factory(x, y) for x in xrange(width)] )
            
        self.nodes = nodes
        
        self._x_wrap = x_wrap
        self._y_wrap = y_wrap        
        
        self._wrap_functions = [ self._make_wrap(self._x_wrap, self.width),
                                 self._make_wrap(self._y_wrap, self.height) ]
        
    
    def _get_x_wrap(self):
        return self._x_wrap
    def _set_x_wrap(self, x_wrap):
        self._x_wrap = x_wrap
        self._wrap_functions[0] = self._make_wrap(self._x_wrap, self.width)
    x_wrap = property(_get_x_wrap, _set_x_wrap, None, "X wrap")
    
    def _get_y_wrap(self):
        return self._y_wrap
    def _set_y_wrap(self, y_wrap):
        self._y_wrap = y_wrap
        self._wrap_functions[1] = self._make_wrap(self._y_wrap, self.width)
    y_wrap = property(_get_y_wrap, _set_y_wrap, None, "Y wrap")
    
    
    def _make_wrap(self, wrap, edge):
        
        if wrap is None or wrap == Wrap.none:
            def do_wrap(value):
                return value
            
        elif wrap == Wrap.repeat:
            def do_wrap(value):
                return value % edge
        
        elif wrap == Wrap.clamp:
            def do_wrap(value):
                if value < 0:
                    return 0
                if value > edge:
                    value = edge
                return value                    
        
        elif wrap == Wrap.error:
            def do_wrap(value):
                return None
            
        else:
            raise ValueError("Unknown wrap mode")
            
        return do_wrap
    
        
    def wrap(self, coord):
        
        x, y = coord
        wrap_x, wrap_y = self._wrap_functions
        return ( wrap_x(x), wrap_y(y) )        
        
    def wrap_x(self, x):
        """Wraps an x coordinate.
        
        x -- X Coordinate
        
        """
        
        return self._wrap_functions[0](x)
        
    def wrap_y(self, y):
        """Wraps a y coordinate.
        
        y -- Y Coordinate.
        
        """
        
        return self._wrap_functions[1](y)
    
    
    def get_size(self):
        
        """Retrieves the size of the grid as a tuple (width, height)."""
        
        return self.width, self.height
        
    def __getitem__(self, coord):        
        
        x, y = coord
        
        if isinstance(x, slice) or isinstance(y, slice):
            if isinstance(x, slice):
                x_indices = x.indices(self.width)
            else:
                x_indices = [x]
                
            if isinstance(y, slice):
                y_indices = y.indices(self.height)
            else:
                y_indices = [y]
                
            try:
                wrap_x = self.wrap_x
                ret = []
                
                for y_index in xrange(*y_indices):
                    nodes_y = self.nodes[ wrap_y(y_index) ]
                    
                    for x_index in xrange(*x_indices):                        
                        ret.append( nodes_y[ wrap_x(x_index) ] )
                        
            except IndexError:
                raise IndexError, "Slice out of range"
            
            return ret
                        
                    
        x, y = self.wrap(coord)            
        
        if x < 0 or y < 0:
            raise IndexError, "coordinate out of range"
        
        try:
            return self.nodes[y][x]
        except IndexError:
            raise IndexError, "coordinate out of range"
    
    def __iter__(self):
        
        for row in self.nodes:
            for node in row:
                yield node
    
    def __contains__(self, value):
        
        for row in self.nodes:
            if node in row:
                return True                
                
        return False
    
    
    def clear(self):
        
        """Resets the grid."""
        
        node_factory = self.node_factory
        
        nodes = []
        
        for y in xrange(height):
            nodes.append( [node_factory(x, y) for x in xrange(width)] )
            
        self.nodes = nodes
        
    
    
    def get(self, x, y, default=None):
        
        """Retrieves a node from the grid.
        
        x -- X coordinate
        y -- Y coordinate
        default -- Default value to use if coord is out of range
        
        """
                
        x, y = self.wrap(coord)
        
        if x < 0 or y < 0 or x >= self.width or y >= self.height:            
            return default
        
        try:
            return self.nodes[y][x]
        except IndexError:
            raise IndexError, "coordinate out of range"
        

    def get_nodes(self, coord, size, wrap=False):
        
        x, y = coord
        x1, y1 = self.wrap(coord)
        w, h = size
        x2, y2 = self.wrap((x+w, y+h))
        
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
                    
        ret = []            
        wrap_x, wrap_y = self._wrap_functions
        
        for y_coord in xrange(y1, y2):
            
            ret += self.nodes[y_coord][x1:x2]                
            
    
        return ret
        
        

if __name__ == "__main__":
    
    class Square(object):
        def __init__(self, x, y):
            self.value = (x, y)
        def __str__(self):
            return str(self.value)
        def __repr__(self):
            return str(self.value)
    
    g = Grid(Square, 100, 100, x_wrap = Wrap.repeat)
        
    print g[10:20, 10:20]
    print g.get_nodes((-2, 0), (5, 5))
    
        