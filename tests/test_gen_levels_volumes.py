from bdns_plus.gen_levels_volumes import gen_levels


def test_gen_levels():
    levels = gen_levels()
    assert len(levels) == 100
