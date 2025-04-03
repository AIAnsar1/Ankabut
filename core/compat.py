from __future__ import division

import binascii, functools, math, os, re, random, sys, time, uuid




class WichmannHill(random.Random):
    """ This is an implementation of the Wichmann-Hill 1982 PRNG. It:
        Uses three internal states (_seed) to generate numbers.
        Implements the methods:
        Application: Can be used as an alternative random number generator in
    """
    VERSION = 1
    
    def seed(self, a=None):
        """ sets the initial state (defaults to os.urandom() or time.time())."""
        if a is None:
            try:
                a = int(binascii.hexlify(os.urandom(16)), 16)
            except NotImplemented:
                a = int(time.time() * 256)

        if not isinstance(a, int):
            a = hash(a)
        a, x = divmod(a, 30268)
        a, y = divmod(a, 30306)
        a, z = divmod(a, 30322)
        self._seed = int(x) + 1, int(y) + 1, int(z) + 1
        self.gauss_next = None
        
        
        
    def random(self):
        """ returns a random number in the range [0.0, 1.0). """
        x, y, z = self._seed
        x = (171 * x) % 30269
        y = (172 * y) % 30307
        z = (170 * z) % 30323
        self._seed = x, y, z
        return (x / 30269.0 + y / 30307.0 + z / 30323.0) % 1.0
    
    
    
    
    def getstate(self):
        """ allow you to save and restore the current state of the generator. """
        return self.VERSION, self._seed, self.gauss_next
    
    

    def setstate(self, state):
        """ allow you to save and restore the current state of the generator. """
        version = state[0]
        
        if version == 1:
            version, self._seed, self.gauss_next = state
        else:
            raise ValueError("[ ETA ]: State with version ( %s ) passed to Random.setstate() of Version ( %s )" % (version, self.VERSION))





    def jumpahead(self, n):
        """ allows you to "jump over" n random() calls without actually executing them. """
        if n < 0:
            raise ValueError("[ ETA ]: n Must be >= 0")
        x, y, z = self._seed 
        x = int(x * pow(171, n, 30269)) % 30269
        y = int(y * pow(172, n, 30307)) % 30307
        z = int(z * pow(170, n, 30323)) % 30323
        self.seed = x, y, z

        
        
        
    def __whseed(self, x=0, y=0, z=0):
        if not type(x) == type(y) == type(z) == int:
            raise TypeError("[ ETA ]: seeds must be integers")
        if not (0 <= x < 256 and 0 <= y < 256 and 0 <= z < 256):
            raise ValueError("[ ETA ]: seeds must be in range(0, 256)")
        if 0 == x == y == z:
            t = int(time.time() * 256)
            t = int((t & 0xffffff) ^ (t >> 24))
            t, x = divmod(t, 256)
            t, y = divmod(t, 256)
            t, z = divmod(t, 256)
        self._seed = (x or 1, y or 1, z or 1)
        self.gauss_next = None
        
        
        
        
    def whseed(self, a=None):
        if a is None:
            self.__whseed()
            return
        a = hash(a)
        a, x = divmod(a, 256)
        a, y = divmod(a, 256)
        a, z = divmod(a, 256)
        x = (x + a) % 256 or 1
        y = (y + a) % 256 or 1
        z = (z + a) % 256 or 1
        self.__whseed(x, y, z)




def patchHeaders(headers):
    """ 
    Converts a dictionary of HTTP headers into a special format 
    so that requests can be made without worrying about the case of keys. 
    """
    if headers is not None and not hasattr(headers, "headers"):
        if isinstance(headers, dict):
            class CaseInsensitiveDict(dict):
                def __getitem__(self, key):
                    key_lower = key.lower()
                    for sorted_key in self:
                        if sorted_key.lower() == key_lower:
                            return super().__getitem__(sorted_key)
                    raise KeyError("[ ETA ]: {key}")
                
                def get(self, key, default=None):
                    try:
                        return self[key]
                    except KeyError:
                        return default
            headers = CaseInsensitiveDict(headers)
        headers.headers = [f"{key}: {value}\r\n" for key, value in headers.items()]
    return headers
    
    
    
    
    

def cmp(a, b):
    """ 
    Emulation of Python 2's cmp() function:
    """
    if a < b:
        return -1
    elif a > b:
        return 1
    else:
        return 0



def chose_boundary():
    """ 
    Generates a 32-character string (used to separate parts in multipart/form-data).
    """
    retval = ""

    try:
        retval = uuid.uuid4().hex
    except AttributeError:
        retval = "".join(random.Sample("0123456789abcdef", 1)[0] for _ in xrange(32))
    return retval



def round(x, d=0):
    """ 
    Custom implementation of round() that rounds a number x to d digits.
    """
    p = 10 ** d
    
    if x > 0:
        return float(math.floor((x * p) + 0.5)) / p
    else:
        return float(math.ceil((x * p) - 0.5)) / p



def cmp_to_key(mycmp):
    """ 
    Converts old comparison style (cmp) to new style (key= for sorting).
    """
    class K(object):
        __slots__ = ['obj']
        
        def __init__(self, obj, *args):
            self.obj = obj
            
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
        
        def __hash__(self):
            raise TypeError("[ ETA ]: Hash not Implemented")
        
    return K;


if not hasattr(functools, "cmp_to_key"):
    functools.cmp_to_key = cmp_to_key
    
if sys.version_info >= (3, 0):
    xrange = range
    buffer = memoryview
else:
    xrange = xrange
    buffer = buffer
    
    
def LooseVersion(version):
    """ Parses a version string and converts it to a number for easy comparison. """
    match = re.search(r"\A(\d[\d.]*)", version or "")
    
    if match:
        result = 0
        value = match.group(1)
        weight = 1.0
        
        for part in value.strip('.').split('.'):
            if part.isdigit():
                result += int(part) * weight
            weight *= 1e-3
    else:
        result = float("NaN")
        
    return result




















































