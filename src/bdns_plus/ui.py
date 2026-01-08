# +
import ipywidgets as w
import traitlets as tr
from ipyautoui.autoobject import AutoObject
from ipyautoui.custom.buttonbars import SaveButtonBar
from ipyautoui.custom.editgrid import EditGrid
from ipyautoui.custom.jsonable_dict import JsonableModel
from ipyautoui.custom.showhide import ShowHide
from IPython.display import display
from pydantic import ValidationError

from bdns_plus.docs import display_tag_data, gen_project_equipment_data
from bdns_plus.gen_idata import gen_config_iref
from bdns_plus.models import (
    Config,
    CustomTagDefList,
    InstanceTag,
    InstanceTagWithoutExtra,
    Levels,
    TagDef,
    TypeTag,
    TypeTagWithoutExtra,
    Volumes,
)
from bdns_plus.tag import simple_tag_with_description

# -

# Constants
HTML_EXAMPLE_STYLE = "padding: 10px; background-color: #f0f0f0; border-radius: 5px;"
HTML_ERROR_STYLE = "padding: 10px; background-color: #fff3cd; border-radius: 5px;"
CUSTOM_TAG_DEF_TITLE = "Create a project specific Equipment Referencing definition (NOT RECOMMENDED)"
LEVEL_MIN, LEVEL_MAX, NO_VOLUMES = -1, 3, 2


class BdnsPlusConfig(w.VBox):
    _value = tr.Dict(
        default_value={
            "volumes": [
                {
                    "id": 1,
                    "code": "ZZ",
                    "name": "Multiple Zones/Sitewide",
                },
            ],
            "levels": [
                {
                    "id": 0,
                    "code": "00",
                    "name": "Level 00",
                },
                {
                    "id": 80,
                    "code": "ZZ",
                    "name": "Multiple Levels",
                },
            ],
            "i_tag": {},
            "t_tag": {},
            "custom_tags": [],
        },
        allow_none=True,
    )
    on_save = tr.Callable(default_value=None, allow_none=True)
    on_revert = tr.Callable(default_value=None, allow_none=True)

    def __init__(self, **kwargs):
        # Extract value before passing kwargs to super
        initial_value = kwargs.pop("value", None)

        self.volume_grid = EditGrid(Volumes)
        self.volume_grid.ui_add.show_null = True
        self.volume_grid.ui_edit.show_null = True

        self.level_grid = EditGrid(Levels)
        self.level_grid.ui_add.show_null = True
        self.level_grid.ui_edit.show_null = True

        self.i_tag_rendered_text = w.HTML("")
        self.i_tag_widget = AutoObject.from_pydantic_model(
            TagDef,
            show_null=True,
            open_nested=True,
            value=InstanceTagWithoutExtra().model_dump(),
        )

        # Determine auto_open for i_tag, t_tag, and custom_tags
        auto_open_i_tag = False
        auto_open_t_tag = False
        auto_open_custom_tags = False
        if "value" in kwargs:
            v = kwargs["value"]
            auto_open_i_tag = "i_tag" in v
            auto_open_t_tag = "t_tag" in v
            auto_open_custom_tags = "custom_tags" in v
        elif initial_value is not None:
            auto_open_i_tag = "i_tag" in initial_value
            auto_open_t_tag = "t_tag" in initial_value
            auto_open_custom_tags = "custom_tags" in initial_value

        self.show_hide_i_tag_widget = ShowHide(
            title=CUSTOM_TAG_DEF_TITLE,
            fn_display=lambda: self.i_tag_widget,
            auto_open=auto_open_i_tag,
        )
        self.i_tag_container = w.VBox([self.i_tag_rendered_text, self.show_hide_i_tag_widget])

        self.t_tag_rendered_text = w.HTML("")
        self.t_tag_widget = AutoObject.from_pydantic_model(
            TagDef,
            show_null=True,
            open_nested=True,
            value=TypeTagWithoutExtra().model_dump(),
        )

        self.show_hide_t_tag_widget = ShowHide(
            title=CUSTOM_TAG_DEF_TITLE,
            fn_display=lambda: self.t_tag_widget,
            auto_open=auto_open_t_tag,
        )
        self.t_tag_container = w.VBox([self.t_tag_rendered_text, self.show_hide_t_tag_widget])

        # Custom tags with info message and ShowHide
        self.custom_tags = JsonableModel(CustomTagDefList)
        self.custom_tags_info = w.HTML(
            "<b>If custom tags are required, please contact your Group/Project Digital Design Engineer</b>",
        )
        self.show_hide_custom_tags = ShowHide(
            title="Show custom tags",
            fn_display=lambda: self.custom_tags,
            auto_open=auto_open_custom_tags,
        )
        self.custom_tags_container = w.VBox(
            [
                self.custom_tags_info,
                self.show_hide_custom_tags,
            ],
        )

        # Examples tab with output widget
        self.examples_output = w.Output()
        self.examples_container = w.VBox(
            [
                w.HTML(
                    "<div style='text-align: center;'><h3>Tag Examples</h3><p>This shows how tags will be generated with your current configuration.</p></div>",
                ),
                self.examples_output,
            ],
        )

        self.tab = w.Tab(
            [
                self.volume_grid,
                self.level_grid,
                self.i_tag_container,
                self.t_tag_container,
                self.custom_tags_container,
                self.examples_container,
            ],
            titles=[
                "Volumes",
                "Levels",
                "Instance Tag",
                "Type Tag",
                "Custom Tags",
                "Examples",
            ],
        )

        self.save_button = SaveButtonBar()
        self.save_button.fns_onsave_add_action(self._on_save_clicked)
        self.save_button.fns_onrevert_add_action(self._on_revert_clicked)

        button_row = w.HBox(
            [self.save_button],
            layout=w.Layout(),
        )

        super().__init__([button_row, self.tab], **kwargs)

        # Set initial value if provided
        if initial_value is not None:
            # Set each tab widget's value if present in initial_value
            if "volumes" in initial_value:
                self.volume_grid.value = initial_value["volumes"]
            if "levels" in initial_value:
                self.level_grid.value = initial_value["levels"]
            if "i_tag" in initial_value:
                self.i_tag_widget.value = initial_value["i_tag"]
                # Open the show/hide widget if i_tag is present
                self.show_hide_i_tag_widget.is_show = True
            if "t_tag" in initial_value:
                self.t_tag_widget.value = initial_value["t_tag"]
                # Open the show/hide widget if t_tag is present
                self.show_hide_t_tag_widget.is_show = True
            if "custom_tags" in initial_value:
                self.custom_tags.value = initial_value["custom_tags"]
                # Open the show/hide widget if custom_tags is present
                self.show_hide_custom_tags.is_show = True
            # Also set the overall config value
            self.value = initial_value

        # Initialize tag examples
        self._update_i_tag_example(None)
        self._update_t_tag_example(None)
        # Only generate examples when Examples tab is selected
        self.tab.observe(self._on_tab_change, names="selected_index")

        if initial_value is None:
            # Initialize value from default _value
            self.volume_grid.value = self._value.get("volumes", [])
            self.level_grid.value = self._value.get("levels", [])
            self.value = self._value

        self._register_observers()

    def _on_tab_change(self, change):
        # Only update examples when Examples tab is selected
        if change["new"] == 5:  # 5 is the index of the Examples tab
            self._update_examples_display()

    def _register_observers(self) -> None:
        """Register all value change observers."""
        widgets = [
            self.volume_grid,
            self.level_grid,
            self.i_tag_widget,
            self.t_tag_widget,
            self.custom_tags,
        ]
        # Observe show/hide for custom tags
        for widget in widgets:
            widget.observe(self._update_value, "_value")

        self.show_hide_i_tag_widget.observe(self._update_value, "is_show")
        self.show_hide_t_tag_widget.observe(self._update_value, "is_show")
        self.show_hide_custom_tags.observe(self._update_value, "is_show")
        self.custom_tags.observe(self._update_value, "has_error")

        # Observe tag widget changes to update examples
        self.i_tag_widget.observe(self._update_i_tag_example, "_value")
        self.t_tag_widget.observe(self._update_t_tag_example, "_value")
        self.show_hide_i_tag_widget.observe(self._update_i_tag_example, "is_show")
        self.show_hide_t_tag_widget.observe(self._update_t_tag_example, "is_show")

    def _update_tag_example(self, widget, show_hide, html_widget, default_tag, example_data) -> None:
        """Shared helper to update tag examples based on current widget values."""
        try:
            tag_def = TagDef(**widget.value)
            if show_hide.is_show:
                example_tag = simple_tag_with_description(example_data, tag_def)
            else:
                example_tag = simple_tag_with_description(example_data, default_tag)
            html_widget.value = f"<div style='{HTML_EXAMPLE_STYLE}'><strong>Example:</strong> {example_tag}</div>"
        except Exception:
            html_widget.value = f"<div style='{HTML_ERROR_STYLE}'><em>Invalid configuration</em></div>"

    def _update_i_tag_example(self, change) -> None:  # noqa: ANN001
        """Update the instance tag example based on current widget values."""
        example_data = {
            "abbreviation": "AHU",
            "volume": "ZZ",
            "level": "XX",
            "volume_level_instance": 1,
        }
        self._update_tag_example(
            self.i_tag_widget,
            self.show_hide_i_tag_widget,
            self.i_tag_rendered_text,
            InstanceTag(),
            example_data,
        )

    def _update_t_tag_example(self, change) -> None:  # noqa: ANN001
        """Update the type tag example based on current widget values."""
        example_data = {
            "abbreviation": "AHU",
            "type_reference": 1,
        }
        self._update_tag_example(
            self.t_tag_widget,
            self.show_hide_t_tag_widget,
            self.t_tag_rendered_text,
            TypeTag(),
            example_data,
        )

    def _update_examples_display(self, change=None) -> None:  # noqa: ANN001
        """Update the examples tab with current configuration. No row limit. Shows a loading spinner while processing."""
        spinner_html = """
            <div style='text-align:center;padding:1em;'>
                <span class='loader' style='display:inline-block;width:2em;height:2em;border:0.3em solid #ccc;border-top:0.3em solid #333;border-radius:50%;animation:spin 1s linear infinite;'></span>
                <style>@keyframes spin{0%{transform:rotate(0deg);}100%{transform:rotate(360deg);}}</style>
                <div>Loading examples...</div>
            </div>
        """
        self.examples_output.clear_output(wait=True)
        with self.examples_output:
            display(w.HTML(spinner_html))
        try:
            # Build config from current values
            config_dict = self.process_data(self.value)
            if not config_dict:
                config_dict = {}

            # Use actual number of volumes from current widget values
            actual_no_volumes = len(self.volume_grid.value) if self.volume_grid.value else NO_VOLUMES
            config_iref = gen_config_iref(level_min=LEVEL_MIN, level_max=LEVEL_MAX, no_volumes=actual_no_volumes)

            # Always show volume in examples, even with single volume (set drop_if_single_volume=False)
            config = Config(**config_iref.model_dump() | config_dict | {"drop_if_single_volume": False})

            # Generate example data
            df = gen_project_equipment_data(config=config)

            # Clear and display
            self.examples_output.clear_output(wait=True)
            with self.examples_output:
                display(display_tag_data(df))
        except Exception as e:  # noqa: BLE001
            self.examples_output.clear_output(wait=True)
            with self.examples_output:
                display(w.HTML(f"<div style='{HTML_ERROR_STYLE}'>Could not generate examples: {e!s}</div>"))

    def _update_value(self, change) -> None:  # noqa: ANN001
        value_dict = {
            "volumes": self.volume_grid.value,
            "levels": self.level_grid.value,
        }

        if self.show_hide_i_tag_widget.is_show:
            value_dict["i_tag"] = self.i_tag_widget.value

        if self.show_hide_t_tag_widget.is_show:
            value_dict["t_tag"] = self.t_tag_widget.value

        if self.show_hide_custom_tags.is_show and not self.custom_tags.has_error:
            value_dict["custom_tags"] = self.custom_tags.value

        self.value = value_dict
        self.save_button.unsaved_changes = True

    def _on_save_clicked(self) -> None:
        """Handle save button click."""
        if self.on_save is not None:
            # Validate all data before saving
            is_valid, errors = self._validate_all_data(self.value)

            if not is_valid:
                # Display validation errors
                error_message = "\n".join(errors)
                print(f"Validation failed:\n{error_message}")
                # You could also show this in UI
                return

            if self.custom_tags.has_error:
                print("Cannot save: There are errors in the Custom Tags configuration.")
                # You could also show this in UI
                return

            # Process and save only if validation passes
            value = self.process_data(self.value)
            self.on_save(value)

    def _on_revert_clicked(self) -> None:
        """Handle revert button click."""
        if self.on_revert is not None:
            self.on_revert()

    def _validate_all_data(self, value: dict) -> tuple[bool, list[str]]:
        """
        Validate all data objects using their pydantic models.

        Returns:
            tuple: (is_valid, error_messages)

        """
        errors = []

        # Validate volumes
        if value.get("volumes"):
            try:
                Volumes.model_validate(value["volumes"])
            except ValidationError as e:
                errors.append(f"Volumes validation error: {e}")

        # Validate levels
        if value.get("levels"):
            try:
                Levels.model_validate(value["levels"])
            except ValidationError as e:
                errors.append(f"Levels validation error: {e}")

        # Validate instance tag
        if value.get("i_tag"):
            try:
                TagDef.model_validate(value["i_tag"])
            except ValidationError as e:
                errors.append(f"Instance tag validation error: {e}")

        # Validate type tag
        if value.get("t_tag"):
            try:
                TagDef.model_validate(value["t_tag"])
            except ValidationError as e:
                errors.append(f"Type tag validation error: {e}")

        # Validate custom tags
        if value.get("custom_tags"):
            try:
                CustomTagDefList.model_validate(value["custom_tags"])
            except ValidationError as e:
                errors.append(f"Custom tags validation error: {e}")

        return len(errors) == 0, errors

    def _validate_and_format_data(self, value: dict) -> dict | None:
        """Validate volumes and levels with pydantic models."""
        if not value:
            return {"volumes": [], "levels": [], "i_tag": {}, "t_tag": {}, "custom_tags": []}

        try:
            volumes_data = value.get("volumes", [])
            levels_data = value.get("levels", [])

            validated_volumes = Volumes.model_validate(volumes_data).model_dump(
                mode="json",
                by_alias=True,
            )
            validated_levels = Levels.model_validate(levels_data).model_dump(
                mode="json",
                by_alias=True,
            )

            return {
                "volumes": validated_volumes,
                "levels": validated_levels,
                **{k: v for k, v in value.items() if k in ["i_tag", "t_tag", "custom_tags"]},
            }
        except ValidationError as e:
            print(f"Validation error: {e}")
            return None

    def process_data(self, value) -> dict | None:
        """Process data before saving."""
        processed = {}
        for k, v in value.items():
            if k == "custom_tags" and v:
                # Remove None fields from each dict and filter out empty dicts
                filtered_tags = [
                    {key: val for key, val in item.items() if val is not None}
                    for item in v
                    if not all(val is None for val in item.values())
                ]
                if filtered_tags:
                    processed[k] = filtered_tags
            elif v:
                processed[k] = v
        return processed

    @property
    def value(self) -> dict:
        """Get the current values from both grids."""
        return self._value

    @value.setter
    def value(self, value) -> None:
        # Always update widgets to match the new value
        volumes = value.get("volumes", [])
        levels = value.get("levels", [])
        self.volume_grid.value = volumes
        self.level_grid.value = levels
        self.show_hide_i_tag_widget.is_show = "i_tag" in value
        self.show_hide_t_tag_widget.is_show = "t_tag" in value
        self.show_hide_custom_tags.is_show = "custom_tags" in value
        data = self._validate_and_format_data(value)
        if data is not None:
            self._value = data


if __name__ == "__main__":

    def on_save(value):
        print("Saving...")
        print(value)

    cnfg = BdnsPlusConfig(on_save=on_save)
    display(cnfg)
