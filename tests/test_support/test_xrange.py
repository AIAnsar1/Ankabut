import pytest

from support.xrange import xrange



def test_basic_usage():
    xr = xrange(1, 10, 2)
    assert list(xr[i] for i in range(len(xr))) == [1, 3, 5, 7, 9]
    assert 5 in xr
    assert 6 not in xr
    assert xr[0] == 1
    assert xr[2] == 5
    assert len(xr) == 5

def test_slice_access():
    xr = xrange(1, 10, 2)
    sliced = xr[1:3]
    assert isinstance(sliced, xrange)
    assert list(sliced[i] for i in range(len(sliced))) == [3, 5]

def test_index_method():
    xr = xrange(1, 10, 2)
    assert xr.index(5) == 2

def test_out_of_bounds():
    xr = xrange(1, 5)
    with pytest.raises(IndexError):
        _ = xr[10]

def test_invalid_args():
    with pytest.raises(TypeError):
        _ = xrange(1, None)

def test_index_method():
    xr = xrange(1, 10, 2)
    assert xr.index(5) == 2
    with pytest.raises(ValueError):
        xr.index(6)

def test_contains():
    xr = xrange(0, 10, 2)
    assert 4 in xr
    assert 5 not in xr

def test_repr_and_hash():
    xr = xrange(0, 5, 1)
    assert repr(xr) == "xrange(0, 5, 1)"
    assert isinstance(hash(xr), int)























