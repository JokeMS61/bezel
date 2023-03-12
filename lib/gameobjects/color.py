from math import *
from util import format_number


class ColorRGBA(object):
    
    __slots__ = ('_c',)
    
    def __init__(self, *args):
        
        """Creates a color object."""
        
        if not args:
            self._c = [0.0, 0.0, 0.0, 1.0]
            return
                
        if len(args) == 1:
            args = args[0]            
        
        if len(args) == 3:
            r, g, b = args
            self._c = [float(r), float(g), float(b), 1.]
            return
        if len(args) == 4:
            r, g, b, a = args
            self._c = [float(r), float(g), float(b), float(a)]
            return
        
        raise ValueError("3 or 4 values required")        
            
    def __str__(self):
                
        return "(" + ", ".join(map(str, self._c)) + ")"
        
    def __repr__(self):
        
        return "ColorRGBA(" + ", ".join(map(str, self._c)) + ")"

    @classmethod
    def black(cls):
        
        """Create a color object representing black."""
        
        c = cls.__new__(cls, object)
        c._c = [0.0, 0.0, 0.0, 1.0]
        return c
    
    @classmethod
    def white(cls):
        
        """Create a color object representing white."""
        
        c = cls.__new__(cls, object)
        c._c = [1.0, 1.0, 1.0, 1.0]
        return c
    
    
    @classmethod
    def from_floats(cls, r, g, b, a=1.0):
        
        """Creates a color object from float components.
        
        r -- Red component
        g -- Green component
        b -- Blue component
        a -- Alpha component
        
        """
                
        c = cls.__new__(cls, object)
        c._c = [r, g, b, a]
        return c
    
    @classmethod
    def from_rgba8(cls, r, g, b, a=255):
        
        """Creates a color object from 4 integer components in 0->255 range.
        
        r -- Red component
        g -- Green component
        b -- Blue component
        a -- Alpha component
        
        """        
        
        c = cls.__new__(cls, object)
        c._c = [r / 255.0, g / 255.0, b / 255.0, a / 255.0]
        return c

    
    @classmethod
    def from_html(cls, col_str, a=1.0):
        
        """Creates a color object from an html style color string.
        
        col_str -- The color string (eg. "#FF0000")
        
        """
        
        if len(col_str) != 7 or col_str[0] != '#':
            raise ValueError("Requires a color encoded in a html style string")
        
        c = cls.__new__(cls, object)
                
        components = col_str[1:3], col_str[3:5], col_str[5:6]
        
        try:    
            c._c = [ int(s, 16) / 255.0 for s in components ] + [ a ]
        except ValueError:
            raise ValueError \
                ("Components should be encoded as two hex characters")
    
    
    @classmethod
    def grey(self, level, a):
        
        level = float(level)
        c = cls.__new__(cls, object)
        c._c = [level, level, level, 1.0]
        return c
    
    def copy(self):
        
        """Returns a copy of the color object."""
        
        c = self.__new__(self.__class__, object)
        c._c = self._c[:]
        return c
    __copy__ = copy
        
    def _get_r(self):
        return self._c[0]
    def _set_r(self, r):
        assert isinstance(r, float), "Must be a float"
        self._c[0] = r
    r = property(_get_r, _set_r, None, "Red component.")

    def _get_g(self):
        return self._c[1]
    def _set_g(self, g):
        assert isinstance(g, float), "Must be a float"
        self._c[1] = g
    g = property(_get_g, _set_g, None, "Green component.")

    def _get_b(self):
        return self._c[2]
    def _set_b(self, b):
        assert isinstance(b, float), "Must be a float"
        self._c[2] = b
    b = property(_get_b, _set_b, None, "Blue component.")

    def _get_a(self):
        return self._c[3]
    def _set_a(self, a):
        assert isinstance(a, float), "Must be a float"
        self._c[3] = a
    a = property(_get_a, _set_a, None, "Alpha component.")
    
    def _get_rgba8(self):        
        r, g, b, a = self._c
        r = min(max(r, 0.0), 1.0) * 255.0
        g = min(max(g, 0.0), 1.0) * 255.0
        b = min(max(b, 0.0), 1.0) * 255.0
        a = min(max(a, 0.0), 1.0) * 255.0
        return (int(r), int(g), int(b), int(a))
    def _set_rgba8(self, rgba):
        r, g, b, a = rgba
        c = self._c
        c[0] = r / 255.0
        c[1] = g / 255.0
        c[2] = b / 255.0
        c[3] = a / 255.0
        return self
    rgba8 = property(_get_rgba8, _set_rgba8, None, "RGBA integer 8 bit format")
    
    def _get_rgb8(self):
        r, g, b, a = self._c
        r = min(max(r, 0.0), 1.0) * 255.0
        g = min(max(g, 0.0), 1.0) * 255.0
        b = min(max(b, 0.0), 1.0) * 255.0        
        return (int(r), int(g), int(b))
    def _set_rgb8(self, rgb):
        r, g, b = rgba
        c = self._c
        c[0] = r / 255.0
        c[1] = g / 255.0
        c[2] = b / 255.0
        c[3] = 1.0
        return self
    rgb8 = property(_get_rgb8, _set_rgb8, None, "RGB integer 8 bit format")  
    
    
    def __len__(self):
        return 4
    
    def __iter__(self):
        return iter(self._c[:])
    
    def __getitem__(self, index):
        try:            
            return self._c[index]            
        except IndexError:
            raise IndexError, "Index must be 0, 1, 2, or 3"
        
    def __setitem__(self, index, value):
        assert isinstance(vale, float), "Must be a float"
        try:
            self._c[index] = value
        except IndexError:
            raise IndexError, "Index must be 0, 1, 2, or 3"
        
    def __eq__(self, rhs):
        
        r, g, b, a = self._c
        rr, gg, bb, aa = rhs
        return r == rr and g == gg and b == bb and a == aa
    
    def __ne__(self, rhs):
        
        r, g, b, a = self._c
        rr, gg, bb, aa = rhs
        return r != rr or g != gg or b != bb or a != aa
    
    def __hash__(self):
        
        return hash(tuple(self._c))
    
    def __add__(self, rhs):
        
        r, g, b, a = self._c
        rr, gg, bb = rhs[:3]
        
        return self.from_floats(r+rr, g+gg, b+bb, a)
    
    def __iadd__(self, rhs):
        
        r, g, b = rhs[:3]
        c = self._c
        c[0] += r
        c[1] += g
        c[2] += b
        return self
    
    def __radd__(self, lhs):
        
        r, g, b, a = self._c        
        rr, gg, bb = lhs[:3]
        return self.from_floats(rr + r, gg + g, bb + b, a)
    
    def __sub__(self, rhs):
        
        r, g, b, a = self._c
        rr, gg, bb = rhs[:3]
        
        return self.from_floats(r - rr, g - gg, b - bb, a)
    
    def __isub__(self, rhs):
        
        r, g, b = rhs[:3]
        c = self._c
        c[0] -= r
        c[1] -= g
        c[2] -= b
        return self
    
    def __rsub__(self, lhs):
        
        r, g, b = self._c        
        rr, gg, bb = lhs
        return self.from_floats(rr - r, gg - g, bb - b, a)
    
    def __mul__(self, rhs):
        
        r, g, b, a = self._c
        return self.from_floats(r * rhs, g * rhs, b * rhs, a)
    
    def __imul__(self, rhs):
        
        c = self._c
        c[0] *= rhs
        c[1] *= rhs
        c[2] *= rhs
        return self
    
    def __rmul__(self, lhs):
        
        r, g, b, a = self._c
        return self.from_floats(lhs / r, lhs / g, lhs / b, a)
            
    def __div__(self, rhs):
        
        r, g, b, a = self._c
        return self.from_floats(r / rhs, g / rhs, b / rhs, a)
    
    def __idiv__(self, rhs):
        
        c = self._c
        c[0] *= rhs
        c[1] *= rhs
        c[2] *= rhs
        return self
    
    def __rdiv__(self, lhs):
        
        r, g, b, a = self._c
        return self.from_floats(lhs / r, lhs / g, lhs / b, a)
    
    def __neg__(self):
        
        r, g, b, a = self._c
        return self.from_floats(-r, -g, -b, a)
    
    def __pos__(self):
        
        return self.copy()
    
    def __nonzero__(self):
        
        r, g, b, a = self._c
        return r and g and b and a
    
    def __call__(self, keys):
        
        c = self._c
        try:
            return tuple(c["rgba".index(k)] for k in keys)
        except ValueError:
            raise IndexError("Keys must be one of r, g, b, a")
        
        
    def as_tuple(self):
        
        return tuple(self._c)
    
    def as_tuple_rgb(self):
                
        return tuple(self._c[:3])
    
    def as_tuple_rgba(self):
                
        return tuple(self._c)
    
    
    def __int__(self):        
        
        r, g, b, a = self.get_saturate() * 255.0
        return (int(a) << 24) | (int(r) << 16) | (int(g) << 8) | int(b)

    
    def as_html(self):
        
        """Returns the color encoded as an html style string."""
          
        r, g, b, a = self.get_saturate() * 255.
        return "#%02X%02X%02X"%(r, g, b)
    
    
    def saturate(self):
        
        """Saturates the color, so that all components are in the range 0->1"""
        
        c = self._c
        r, g, b, a = c
        c[0] = min(max(r, 0.0), 1.0)
        c[1] = min(max(g, 0.0), 1.0)
        c[2] = min(max(b, 0.0), 1.0)
        c[3] = min(max(a, 0.0), 1.0)
        
    def get_saturate(self):
        
        """Returns the saturated color as a copy."""
        
        col_copy = self.copy()
        c = col_copy._c
        
        r, g, b, a = c
        c[0] = min(max(r, 0.0), 1.0)
        c[1] = min(max(g, 0.0), 1.0)
        c[2] = min(max(b, 0.0), 1.0)
        c[3] = min(max(a, 0.0), 1.0)
        
        return col_copy
    
    def invert(self):
        
        """Inverts the color."""
        
        c = self._c
        r, g, b, a = c
        c[0] = 1.0 - r
        c[1] = 1.0 - g
        c[2] = 1.0 - b
        
    def get_inverse(self):
        
        """Gets the inverse of the color."""
        
        col_copy = self.copy()
        
        c = col_copy._c
        r, g, b, a = c
        c[0] = 1.0 - r
        c[1] = 1.0 - g
        c[2] = 1.0 - b
        
        return col_copy
    
    def mul_alpha(self):
        
        """Multiplies the color by its alpha component."""
        
        c = self._c
        a = c[3]
        c[0] *= a
        c[1] *= a
        c[2] *= a

Color = ColorRGBA  
    
    
        
class Palette:
    
    """Contains a number of pre-defined colors."""
    
    black =     (0.0, 0.0, 0.0)
    blue =      (0.0, 0.0, 1.0)
    green =     (0.0, 1.0, 0.0)
    cyan =      (0.0, 1.0, 1.0)
    red =       (1.0, 0.0, 0.0)
    magenta =   (1.0, 0.0, 1.0)
    yellow =    (1.0, 1.0, 0.0)
    white =     (1.0, 1.0, 1.0)

    grey25 =    (0.25, 0.25, 0.25)
    grey50 =    (0.5, 0.5, 0.5)
    grey75 =    (0.75, 0.75, 0.75)
        
  

if __name__ == "__main__":
    
    c1 = Color(.5, .2, .8)
    c2 = Color(1., 0., .2)
    print c1
    print repr(c1)
    print int(c1)
    print c1+c2
    print Color.white()
    print c1('rrrgggbbbaaa')