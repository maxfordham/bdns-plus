import pathlib
import re

from bdns_plus.abbreviations import get_bdns_asset_abbreviations

MYDIR = pathlib.Path(__file__).parent.resolve()


def get_unique_ifc4_3_classes() -> set[str]:
    abbreviations = get_bdns_asset_abbreviations()
    cols = abbreviations[0]
    n = cols.index("ifc4_3")
    return set([x[n] for x in abbreviations[1:] if x[n]])  # type: ignore[union-attr]


def ifc_class_drop_enum(s: str) -> str:
    """Remove IFC class enum suffixes from class names."""
    # Remove IFC class enum suffixes like 'Enum' or 'ENUM'
    return re.sub(r"([A-Z0-9_]+_?)$", "", s)


# Example usage:
if __name__ == "__main__":
    unique_classes = get_unique_ifc4_3_classes()
    unique_classes = {ifc_class_drop_enum(x) for x in unique_classes}

    (MYDIR / "bdns_unique_ifc_classes.txt").write_text("\n".join(sorted(unique_classes)))
    print(unique_classes)
