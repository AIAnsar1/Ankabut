import pytest
from core.compat import WichmannHill, patchHeaders, cmp, chose_boundary, round, cmp_to_key, LooseVersion


def test_wichmannhill_random():
    rng = WichmannHill()
    rng.seed(12345)
    r1 = rng.random()
    r2 = rng.random()
    assert 0.0 <= r1 < 1.0
    assert 0.0 <= r2 < 1.0
    assert r1 != r2  # Проверка, что генератор действительно случайный

def test_wichmannhill_seed():
    rng1 = WichmannHill()
    rng1.seed(42)
    rng2 = WichmannHill()
    rng2.seed(42)
    assert rng1.random() == rng2.random()  # Должны совпадать при одинаковом seed

def test_wichmannhill_getset_state():
    rng = WichmannHill()
    rng.seed(123)
    state = rng.getstate()
    r1 = rng.random()
    rng.setstate(state)
    r2 = rng.random()
    assert r1 == r2  # После восстановления состояния числа должны совпадать

def test_wichmannhill_jumpahead():
    rng = WichmannHill()
    rng.seed(123)
    r1 = rng.random()
    rng.jumpahead(5)
    r2 = rng.random()
    assert r1 != r2  # Проверка, что прыжок реально изменяет последовательность

def test_patchHeaders():
    headers = {"Content-Type": "application/json", "User-Agent": "pytest"}
    patched = patchHeaders(headers)
    assert patched["content-type"] == "application/json"
    assert patched["user-agent"] == "pytest"

def test_cmp():
    assert cmp(1, 2) == -1
    assert cmp(2, 1) == 1
    assert cmp(3, 3) == 0

def test_chose_boundary():
    boundary = chose_boundary()
    assert isinstance(boundary, str)
    assert len(boundary) == 32

def test_round():
    assert round(1.23456, 2) == 1.23
    assert round(-1.23456, 2) == -1.23
    assert round(1.5) == 2
    assert round(-1.5) == -2

def test_cmp_to_key():
    items = [3, 1, 4, 1, 5, 9, 2]
    sorted_items = sorted(items, key=cmp_to_key(lambda a, b: a - b))
    assert sorted_items == [1, 1, 2, 3, 4, 5, 9]

def test_loose_version():
    assert LooseVersion("1.2.3") < LooseVersion("1.2.4")
    assert LooseVersion("2.0") > LooseVersion("1.9.9")
    assert LooseVersion("1.10") > LooseVersion("1.2")



if __name__ == "__main__":
    pytest.main()
