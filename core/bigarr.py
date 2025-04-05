
import os, sys, zlib, itertools, tempfile, pickle


from .exceptions import AnkabSystemException
from .compat import xrange
from .enums import MKStempPrefix
from .settings import BIGARRAY_CHUNK_SIZE, BIGARRAY_COMPRESS_LEVEL



try:
    DEFAULT_SIZE_OF = sys.getsizeof(object())
except TypeError:
    DEFAULT_SIZE_OF = 16
    
    
    
    
def _size_of(instance):
    """ This method recursively calculates the size of the passed object, including nested structures (dict, list, tuple). """
    retval = sys.getsizeof(instance, DEFAULT_SIZE_OF)
    
    if isinstance(instance, dict):
        retval += sum(_size_of(_) for _ in itertools.chain.from_iterable(instance.items()))
    elif hasattr(instance, "__iter__"):
        retval += sum(_size_of(_) for _ in instance if _ != instance)
    
    return retval





class Cache(object):
    """ This class is used to temporarily store a chunk loaded from disk."""
    def __init__(self, index, data, dirty):
        self.index = index
        self.data = data
        self.dirty = dirty





class BigArray(list):
    def __init__(self, items=None):
        self.chunks = [[]] # list of lists. Each nested list is a chunk of data.
        self.chunk_length = sys.maxsize
        self.cache = None
        self.filenames = set()
        self._os_remove = os.remove
        self._size_counter = 0
        
        for item in (items or []):
            self.append(item)
            
    
    def __add__(self, value):
        retval = BigArray(self)
        
        for _ in value:
            retval.append(_)
        return retval
    
    
    def __iadd__(self, value):
        for _ in value:
            self.append(_)
        return self
    
    
    def append(self, value):
        """ Add element Adds an element to the last chunk. 
        If the chunk is too big (BIGARRAY_CHUNK_SIZE), 
        it is written to a file (_dump()), and chunks[-1] is replaced with the file name.
        """
        self.chunks[-1].append(value)
        
        if self.chunk_length == sys.maxsize:
            self._size_counter += _size_of(value)
            
            if self._size_counter >= BIGARRAY_CHUNK_SIZE:
                self.chunk_length = len(self.chunks[-1])
                self._size_counter = None
        if len(self.chunks[-1]) >= self.chunk_length:
            filename = self._dump(self.chunks[-1])
            self.chunks[-1] = filename
            self.chunks.append([])
            
            
    def extend(self, value):
        for _ in value:
            self.append(_)
            
            
    def pop(self):
        if len(self.chunks[-1]) < 1:
            self.chunks.pop()
            
            try:
                with open(self.chunks[-1], "rb") as f:
                    self.chunks[-1] = pickle.loads(zlib.decompress(f.read()))
            except IOError as ex:
                errMsg = "exception occurred while retrieving data" 
                errMsg += "from a temporary file ('%s')" % ex
                raise AnkabSystemException(errMsg)
        return self.chunks[-1].pop()




    def index(self, value):
        for index in range(len(self)):
            if self[index] == value:
                return index
        raise ValueError("%s is not in list" % value)
    
    
    
    def _dump(self, chunk):
        """ Write chunk to disk Creates a temporary file. Serializes and compresses data before If an error occurs, throws an exception. writing. """
        try:
            handle, filename = tempfile.mkstemp(prefix=MKStempPrefix.BIG_ARRAY)
            self.filenames.add(filename)
            os.close(handle)
            
            with open(filename, "w+b") as f:
                f.write(zlib.compress(pickle.dumps(chunk, pickle.HIGHEST_PROTOCOL), BIGARRAY_COMPRESS_LEVEL))
            return filename
        except (OSError, IOError) as ex:
            errMsg = "exception occurred while storing data "
            errMsg += "to a temporary file ('%s'). Please " % ex
            errMsg += "make sure that there is enough disk space left. If problem persists, "
            errMsg += "try to set environment variable 'TEMP' to a location "
            errMsg += "writeable by the current user"
            raise AnkabSystemException(errMsg)
        
    
    def _checkcache(self, index):
        """ Checking and loading a chunk from disk If there is changed data (dirty=True), 
        it is first written to disk. If the required chunk is not in memory, 
        it is loaded from disk and unpacked.
        """
        if (self.cache and self.cache.index != index and self.cache.dirty):
            filename = self._dump(self.cache.data)
            self.chunks[self.cache.index] = filename
        if not (self.cache and self.cache.index == index):
            try:
                with open(self.chunks[index], "rb") as f:
                    self.cache = Cache(index, pickle.loads(zlib.decompress(f.read())), False)
            except Exception as ex:
                errMsg = "exception occurred while retrieving data "
                errMsg += "from a temporary file ('%s')" % ex
                raise AnkabSystemException(errMsg)
    
    
    def __getstate__(self):
        return self.chunks, self.filenames
    
    
    def __setstate__(self, state):
        self.__init__()
        self.chunks, self.filenames = state
        
    
    def __getitem__(self, y):
        """ Getting an element Calculates which chunk the element is in. 
        If the chunk is in memory, simply returns the value. 
        If the chunk is in a file, loads it into the cache and returns the element.
        """
        while y < 0:
            y += len(self)
        index = y // self.chunk_length
        offset = y % self.chunk_length
        chunk = self.chunks[index]
        
        if isinstance(chunk, list):
            return chunk[offset]
        else:
            self._checkcache(index)
            return self.cache.data[offset]
        
    def __setitem__(self, y, value):
        index = y // self.chunk_length
        offset = y % self.chunk_length
        chunk = self.chunks[index]
        
        if isinstance(chunk, list):
            chunk[offset] = value
        else:
            self._checkcache(index)
            self.cache.data[offset] = value
            self.cache.dirty = True
    
    
    def __repr__(self):
        return "%s%s" % ("..." if len(self.chunks) > 1 else "", self.chunks[-1].__repr__())
    
    
    def __iter__(self):
        for i in xrange(len(self)):
            try:
                yield self[i]
            except IndexError:
                break
            
            
    def __len__(self):
        return len(self.chunks[-1]) if len(self.chunks) == 1 else (len(self.chunks) - 1) * self.chunk_length + len(self.chunks[-1])























