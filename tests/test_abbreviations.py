from bdns_plus.abbreviations import get_bdns_asset_abbreviations


def test_get_bdns_asset_abbreviations():
    data = get_bdns_asset_abbreviations()
    assert data[0] == [
        "asset_description",
        "asset_abbreviation",
        "can_be_connected",
        "dbo_entity_type",
        "ifc4_3",
        "ifc2x3",
    ]
