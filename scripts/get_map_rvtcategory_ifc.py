import csv
import pathlib

import pandas as pd

MYDIR = pathlib.Path(__file__).parent.resolve()


def read_data():
    fpth = MYDIR / "R25/exportlayers-ifc-IAI.txt"
    with open(fpth, encoding="utf-16") as csvfile:
        reader = csv.reader(csvfile, delimiter="	", quotechar="|")
        data = [row for row in reader]
        header = [row for row in data if row[0][0] == "#"]
        rows = [row for row in data if row[0][0] != "#"]
    return header, rows


def clean_data(rows: list[list]):
    columns = ["rvt-category", "rvt-subcategory", "IfcClass", "IfcType"]
    map_cols = dict(zip(range(len(columns)), columns, strict=False))
    df = pd.DataFrame(data=rows, columns=None)
    df = df.rename(columns=map_cols)
    df = df[columns]
    return df


header, rows = read_data()
df = clean_data(rows)
df.to_csv(MYDIR / "R25-map-rvtcategory-ifc.csv", index=None)
