import yaml


# ------------------------------
def str_presenter(dumper, data):
    """Configure yaml for dumping multiline strings.

    Ref: https://stackoverflow.com/questions/8640959/how-can-i-control-what-scalar-form-pyyaml-uses-for-my-data.
    """
    if len(data.splitlines()) > 1:  # check for multiline string
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


yaml.add_representer(str, str_presenter)
yaml.representer.SafeRepresenter.add_representer(
    str,
    str_presenter,
)  # to use with safe_dum
# ------------------------------
# ^ configures yaml for pretty dumping of multiline strings


def data_as_yaml_markdown(data: dict) -> str:
    return f"""
```yaml
{yaml.dump(data, sort_keys=False, indent=2)}
```
"""
