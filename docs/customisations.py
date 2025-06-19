# %% [markdown]
# ---
# title: Customisations
# execute:
#   echo: false
# format:
#   html:
#     code-fold: true
# ---

# %% [markdown]
"""
`bdns-plus` is designed to "just-work" and assumes a set of sensible defaults.
That said, it is also possible to configure `bdns-plus` to better suit your projects requirements.
Configuration is achieved through the setting of environment variables, defined below.

## Default Configuration Properties

When using the `bdns-plus` python package, the following properties are used by default:
"""

# %%
import ipywidgets as w
import pandas as pd
from ipydatagrid import DataGrid
from IPython.display import display

from bdns_plus.docs import display_config_summary
from bdns_plus.models import Config

config = Config()
display_config_summary(config)

# %% [markdown]
"""
This configuration can be represented as a single JSON object, which can be loaded dynamically and configured per project.

"""
# %%
from IPython.display import Markdown

from bdns_plus.docs import data_as_json_markdown, markdown_callout

json_str = data_as_json_markdown(config.model_dump(mode="json"))
title = "Tag Definition as json data. Can be loaded dynamically and configured per project."
display(
    Markdown(markdown_callout(json_str, title=title)),
)


# %% [markdown]
"""
## Project Configuration

::: {.callout-tip}
Refer to [examples](examples) for how to use the project configuration.
:::


It is possible to define a project custom configuration file, which can be loaded dynamically.
This is set by defining the environment variable `BDNS_PLUS_CONFIG` to point to a JSON file or URL endpoint.
It can be reloaded dynamically by calling the `bdns_plus.reload_config()` function.

Example of a custom configuration file:

"""
