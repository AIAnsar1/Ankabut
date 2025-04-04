import os, tempfile, pytest

from core.exceptions import AnkabSystemException
from support.bigarr import BigArray


"""

def test_bigarray_append():
    arr = BigArray()
    arr.append(10)
    assert arr[0] == 10



def test_bigarray_extend():
    arr = BigArray()
    arr.extend([1,2,3])
    assert list(arr) == [1,2,3]



def test_bigarray_pop():
    arr = BigArray([1,2,3])
    assert arr.pop() == 3
    assert len(arr) == 2


def test_bigarray_index():
    arr = BigArray([10,20,30])
    assert arr.index(20) == 1

    with pytest.raises(ValueError):
        arr.index(40)



def test_bigarray_serilization():
    arr = BigArray(["a","b","c"])
    state = arr.__getstate__()
    new_arr = BigArray()
    new_arr.__setstate__(state)
    assert list(new_arr) == ["a","b","c"]



def test_bigarray_disk_storage():
    arr = BigArray()
    arr.append("large_data")
    arr._dump(arr.chunks[-1])
    assert os.path.exists(next(iter(arr.filenames)))



def test_bigarray_out_of_bounds():
    arr = BigArray([1,2,3])

    with pytest.raises(IndexError):
        _ = arr[10]



def test_bigarray_cache_handling():
    arr = BigArray([1,2,3,4,5])
    arr._checkcache(0)
    assert arr.cache.index == 0
    
    
"""


def test_bigarray_append():
    arr = BigArray()
    arr.append(10)
    assert arr[0] == 10

def test_bigarray_extend():
    arr = BigArray()
    arr.extend([1, 2, 3])
    assert list(arr) == [1, 2, 3]
    
    
def test_bigarray_getitem():
    arr = BigArray([10, 20, 30])
    assert arr[0] == 10
    assert arr[1] == 20
    assert arr[2] == 30

def test_bigarray_setitem():
    arr = BigArray([10, 20, 30])
    arr[0] = 100
    arr[1] = 200
    arr[2] = 300
    assert arr[0] == 100
    assert arr[1] == 200
    assert arr[2] == 300
    
def test_bigarray_index():
    arr = BigArray([10, 20, 30])
    assert arr.index(20) == 1
    assert arr.index(30) == 2
    with pytest.raises(ValueError):
        arr.index(40)
        
def test_bigarray_disk_storage():
    arr = BigArray()
    arr.append("large_data")
    arr._dump(arr.chunks[-1])
    assert os.path.exists(next(iter(arr.filenames)))

def test_bigarray_pop():
    arr = BigArray([1, 2, 3])
    assert arr.pop() == 3
    assert len(arr) == 2
    
    
def test_bigarray_out_of_bounds():
    arr = BigArray([1, 2, 3])
    with pytest.raises(IndexError):
        _ = arr[10]
        
def test_bigarray_serialization():
    arr = BigArray([1, 2, 3])
    state = arr.__getstate__()
    new_arr = BigArray()
    new_arr.__setstate__(state)
    assert list(new_arr) == [1, 2, 3]