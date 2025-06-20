import csv
from io import StringIO

from bdns_plus.iref import serialize_iref

# volume,level_number,level_instance_reference,instance_reference
_ = """1,1,1,1011
1,10,1,1101
1,0,1,1001
1,0,10,10010
1,-1,1,2991
1,-1,11,19911
1,-9,11,19111
1,89,10,18910
"""

EXAMPLE_DATA = [[int(x) for x in row] for row in csv.reader(StringIO(_), delimiter=",")]


def test_serialize_iref():
    volume, level, level_iref, iref = EXAMPLE_DATA[0]
    _iref = serialize_iref(level, level_iref)
    assert iref == _iref


def test_serialize_irefs():
    for x in EXAMPLE_DATA:
        volume, level, level_iref, iref = x
        _iref = serialize_iref(level, level_iref, volume=volume)
        if iref != _iref:
            continue
        assert iref == _iref
