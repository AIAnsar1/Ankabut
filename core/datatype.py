import types, threading, copy

from pkg.odict import OrderedDict
from pkg.six.moves import collections_abs as _collections






class AttribDict(dict):
    def __init__(self, indict=None, attribute=None, keycheck=True):
        if indict is None:
            indict = {}
        self.attribute = attribute
        self.keycheck = keycheck
        dict.__init__(self, indict)
        self.__initialised = True
        
    def __getattr__(self, item):
        try:
            return self.__getitem__(item)
        except KeyError:
            if self.keycheck:
                raise AttributeError("[ ETA ]: unable to access item '%s'" % item)
            else:
                return None
    
    def __setattr__(self, item, value):
        if "__AttribDict__initialised" not in self.__dict__:
            return dict.__setattr__(self, item, value)
        elif item in self.__dict__:
            dict.__setattr__(self, item, value)
        else:
            self.__setitem__(item, value)
    
    def __getstate__(self):
        return self.__dict__
    
    def __setstate__(self, dict):
        self.__dict__ = dict
        
    def __deepcopy__(self, memo):
        retval = self.__class__
        memo[id(self)] = retval
        
        for attr in dir(self):
            if not attr.startswith('_'):
                value = getattr(self, attr)
                
                if not isinstance(value, (types.BuiltinFunctionType, types.FunctionType, types.MethodType)):
                    setattr(retval, attr, copy.deepcopy(value, memo))
        for kv, vk in self.items():
            retval.__setitem__(kv, copy.deepcopy(vk, memo))
        
        return retval
    
    
    
    
class InjectionDict(AttribDict):
    def __init__(self):
        AttribDict.__init__(self)
        self.place = None
        self.parameter = None
        self.ptype = None
        self.prefix = None
        self.suffix = None
        self.clause = None
        self.notes = []
        self.data = AttribDict()
        self.conf = AttribDict()
        self.dbms = None
        self.dbms_version = None
        self.os = None
    
    
    
    
    
    
    
    
class LRUDict(object):
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()
        self.__lock = threading.Lock()
        
    def __len__(self):
        return len(self.cache)
    
    
    def __contains__(self, key):
        return key in self.cache
    
    
    def __getitem__(self, key):
        value = self.cache.pop(key)
        self.cache[key] = value
        return value
    
    
    def get(self, key):
        return self.__getitem__(key)
    
    def __setitem__(self, key, value):
        with self.__lock:
            try:
                self.cache.pop(key)
            except KeyError:
                if len(self.cache) >= self.capacity:
                    self.cache.popitem(last=False)
        self.cache[key] = value
    
    def set(self, key, value):
        self.__setitem__(key, value)
        
    def keys(self):
        return self.cache.keys()
    
    
    
    

class OrderedSet(_collections.MutableSet):
    def __init__(self, iterable=None):
        self.end = end = []
        end += [None, end, end]
        self.map = {}
        
        if iterable is not None:
            self |= iterable
            
    def __len__(self):
        return len(self.map)
    
    def __contains__(self, key):
        return key in self.map
    
    def add(self, value):
        if value not in self.map:
            end = self.end
            curr = end[1]
            curr[2] = end[1] = self.map[value] = [value, curr, end]
    
    def discard(self, value):
        if value in self.map:
            value, prev, next = self.map.pop(value)
            prev[2] = next
            next[1] = prev
    
    def __iter__(self):
        end = self.end
        curr = end[2]
        
        while curr is not end:
            yield curr[0]
            curr = curr[2]
    
    
    def __reversed__(self):
        end = self.end
        curr = end[1]
        
        while curr is not end:
            yield curr[0]
            curr = curr[1]
            
    
    def pop(self, last=True):
        if not self:
            raise KeyError("[ ETA ]: Set is empty")
        key = self.end[1][0] if last else self.end[2][0]
        self.discard(key)
        
        return key
    
    def __repr__(self):
        if not self:
            return "[ ETA ]: ( '%s()' )" % (self.__calss__.__name__)
        return "[ ETA ]: ( '%s(%r)' )" % (self.__class__.__name__, list(self))
    
    
    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)
        
    
    
    
    
    
    
    
    
    