import numbers



class xrange(object):
    __slots__ = ['_slice']
    
    
    def __init__(self, *args):
        if args and isinstance(args[0], type(self)):
            self._slice = slice(args[0].start, args[0].stop, args[0].step)
        else:
            self._slice = slice(*args)
            
        if self._slice.stop is None:
            raise TypeError("[ ETA ]: xrange stop must not be None")
        
        if self._slice.step is None:
            self._slice = slice(self._slice.start, self._slice.stop, 1)
        
    
    @property
    def start(self):
        """Returns the initial value of the range (start)."""
        if self._slice.start is not None:
            return self._slice.start
        return 0
    
    
    @property
    def stop(self):
        """Returns the end value of the range (stop)."""
        return self._slice.stop
    
    
    @property
    def step(self):
        """Returns the range step (step)."""
        if self._slice.start is not None:
            return self._slice.step
        return 1
    
    
    
    def __hash__(self):
        return hash(self._slice)
    
    def __repr__(self):
        return '%s(%r, %r, %r)' % (type(self).__name__, self.start, self.stop, self.step)
    
    def __len__(self):
        return self._len()
    
    def _len(self):
        """
        Calculates the number of elements in a range.

        Returns:
        - int: length of the range (e.g. for xrange(1, 10, 2) → 5).
        """
        return max(0, 1 + int((self.stop -1 - self.start) // self.step))
    
    def __contains__(self, value):
        """
        Checks if an element is in a range.

        Arguments:
        - item (int): the value to check.

        Returns:
        - bool: True if the element is in the range, False otherwise.
        """
        return (self.start <= value < self.stop) and (value - self.start) % self.step == 0
    
    
    def __getitem__(self, index):
        """
        Returns the element by index, supports negative indices.

        Arguments:
        - index (int): the index of the element, can be negative.

        Returns:
        - int: the element at the specified index.

        Exceptions:
        - IndexError if the index is out of range.
        """
        if isinstance(index, slice):
            start, stop, step = index.indices(self._len())
            return xrange(self._index(start), self._index(stop), step * self.step)
        elif isinstance(index, numbers.Integral):
            if index < 0:
                fixed_index = index + self._len()
            else:
                fixed_index = index
            
            if not 0 <= fixed_index < self._len():
                raise IndexError("[ ETA ]: Index %d out of %r" % (index, self))
            
            return self._index(fixed_index)
        else:
            raise TypeError("[ ETA ]: xrange indices must be slices or integers")
        
    
    def _index(self, i):
        return self.start + self.step * i
    
    """ def index(self, i):
        if self.start <= i < self.stop:
            return i - self.start
        else:
            raise ValueError("[ ETA ]: ( %d ) is not in list" % i) """ 
            
    def index(self, i):
        """
        Returns the index of the element in the range (position from left to right).

        Arguments:
        - i (int): the value whose position to find.

        Returns:
        - int: the index of the element in the range.

        Exceptions:
        - ValueError if the element is not found in the range.
        """
        if self.step > 0:
            in_range = self.start <= i < self.stop
        else:
            in_range = self.start >= i > self.stop

        if not in_range or (i - self.start) % self.step != 0:
            raise ValueError("[ ETA ]: (%d) is not in list" % i)

        return (i - self.start) // self.step