from importlib.resources import files
from frictionless import Package, Resource
from frictionless import describe

DIR_PKG = files("example")
PTH_PKG = DIR_PKG.joinpath("datapackage.yaml")
PTH_LEVELS = DIR_PKG.joinpath("levels.csv")
PTH_VOLUMES = DIR_PKG.joinpath("volumes.csv")

res_levels = Resource(
    path=PTH_LEVELS.name,
    name="levels",
    schema=describe(PTH_LEVELS, type='schema'),
)

res_volumes = Resource(
    path=PTH_VOLUMES.name,
    name="volumes",
    schema=describe(PTH_VOLUMES, type='schema'),
)


description = """project config"""
pkg = Package(
    name='bdns-plus',
    resources=[res_levels, res_volumes]) # from a descriptor


pkg.to_yaml(PTH_PKG) # Save as YAML
print("done")