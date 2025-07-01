import re

import bsdd

IFC4X3_URI = "https://identifier.buildingsmart.org/uri/buildingsmart/ifc/4.3"


def ifc_strip_enum(ifc_class: str) -> str:
    return re.sub(r"([A-Z0-9_]+_?)$", "", ifc_class)


def ifc_class_is_enum(ifc_class: str) -> bool:
    return ifc_strip_enum(ifc_class) != ifc_class


def get_ifc_entities_only(ifc_classes: dict[str, dict]) -> dict[str, dict]:
    """Return only IFC entities, i.e. classes that are not enumerations."""
    return {k: v for k, v in ifc_classes.items() if not ifc_class_is_enum(k)}


def get_ifc_classes(client: bsdd.Client = None) -> dict[str, dict]:
    if client is None:
        client = bsdd.Client()

    def _get_batch(i: int) -> list:
        return client.get_classes(
            IFC4X3_URI,
            use_nested_classes=False,
            class_type="Class",
            offset=i[0],
            limit=i[1],
        )["classes"]

    ifc_classes = {}
    for i in [(0, 1000), (1000, 2000)]:  # 1418 classes in total. 1000 max request limit
        ifc_classes = ifc_classes | {x["code"]: x for x in _get_batch(i)}
    return ifc_classes


def get_ifc_entities(client: bsdd.Client = None) -> dict[str, dict]:
    """Return only IFC entities, i.e. classes that are not enumerations."""
    ifc_classes = get_ifc_classes(client)
    return get_ifc_entities_only(ifc_classes)
