from bdns_plus.abbreviations import AbbreviationsEnum, get_bdns_asset_abbreviations


def test_AbbreviationsEnum():  # noqa: N802
    assert AbbreviationsEnum.AHU == "AHU"


def test_get_bdns_asset_abbreviations():
    data = get_bdns_asset_abbreviations()
    assert data[0] == [
        "asset_description",
        "asset_abbreviation",
        "dbo_entity_type",
        "ifc_class",
        "ifc_type",
        "can_be_connected",
    ]



