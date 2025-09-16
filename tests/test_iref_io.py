import csv
from io import StringIO

from bdns_plus.iref_io import deserialize_iref, get_next_iref, serialize_iref

# level_number,volume_level_instance,instance_reference
_ = """1,1,101
10,1,1001
0,1,9001
0,10,90010
-1,1,9101
-1,11,91011
-9,11,99011
89,10,89010
"""

EXAMPLE_DATA = [[int(x) for x in row] for row in csv.reader(StringIO(_), delimiter=",")]


def test_serialize_iref():
    level, volume_level_instance, iref = EXAMPLE_DATA[0]
    _iref = serialize_iref(level, volume_level_instance)
    assert iref == _iref


def test_serialize_irefs():
    for x in EXAMPLE_DATA:
        level, volume_level_instance, iref = x
        _iref = serialize_iref(level, volume_level_instance)
        assert iref == _iref


def test_deserialize_iref():
    level, volume_level_instance, iref = EXAMPLE_DATA[3]
    _level, _volume_level_instance = deserialize_iref(iref)
    assert (level, volume_level_instance) == (_level, _volume_level_instance)


def test_deserialize_irefs():
    for x in EXAMPLE_DATA:
        level, volume_level_instance, iref = x
        _level, _volume_level_instance = deserialize_iref(iref)
        assert (level, volume_level_instance) == (_level, _volume_level_instance)


def test_get_next_iref():
    iref = get_next_iref([1, 2, 3])
    assert iref == 4
    iref = get_next_iref([1, 2, 3], level_number=3)
    assert iref == 301
    iref = get_next_iref([101, 102, 201], level_number=1)
    assert iref == 103
    iref = get_next_iref([101, 201, 9001], level_number=0)
    assert iref == 9002
    iref = get_next_iref([101, 201, 9101], level_number=-1)
    assert iref == 9102
