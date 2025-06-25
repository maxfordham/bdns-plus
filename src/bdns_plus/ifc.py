import re

import bsdd

IFC4X3_URI = "https://identifier.buildingsmart.org/uri/buildingsmart/ifc/4.3"


def ifc_strip_enum(ifc_class: str) -> str:
    return re.sub(r"([A-Z0-9_]+_?)$", "", ifc_class)


def ifc_class_is_enum(ifc_class: str) -> bool:
    return ifc_strip_enum(ifc_class) != ifc_class


def get_ifc_classes(client=None):
    if client is None:
        client = bsdd.Client()

    def get_batch(i):
        return client.get_classes(
            IFC4X3_URI,
            use_nested_classes=False,
            class_type="Class",
            offset=i[0],
            limit=i[1],
        )["classes"]

    ifc_classes = {}
    for i in [(0, 1000), (1000, 2000)]:  # 1418 classes in total. 1000 max request limit
        ifc_classes = ifc_classes | {x["code"]: x for x in get_batch(i)}
    return ifc_classes
