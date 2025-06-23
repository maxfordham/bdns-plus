"""radiply create examples of iinstance refs equipment in building projects."""

from itertools import chain

from .gen_levels_volumes import gen_levels_config, gen_volumes_config
from .models import ConfigIref, GenDefinition, ITagData, Level, Volume, to_records


def gen_config_iref(level_min: int, level_max: int, no_volumes: int = 1) -> ConfigIref:
    levels = [Level(**x) for x in to_records(gen_levels_config(level_min=level_min, level_max=level_max))]
    volumes = [Volume(**x) for x in to_records(gen_volumes_config(no_volumes=no_volumes))]
    return ConfigIref(levels=levels, volumes=volumes)


def next_iref():  # TODO: implement
    pass


def gen_idata(
    gen_def: GenDefinition,
    config: ConfigIref | None = None,
) -> list[ITagData]:
    """Generate tag data - mostly used for testing and documentation purposes."""
    if config is None:
        config = ConfigIref()

    on_volumes = gen_def.on_volumes
    if on_volumes is None:  # all volumes
        on_volumes = [x.code for x in config.volumes]

    on_levels = gen_def.on_levels
    if on_levels is None:  # all levels
        on_levels = [x.code for x in config.levels]

    items = []
    for v in on_volumes:
        for x in on_levels:
            for i in range(1, gen_def.no_items + 1):
                if isinstance(gen_def.abbreviation, list):
                    if isinstance(gen_def.types, list):
                        assert len(gen_def.abbreviation) == len(gen_def.types), (
                            "If abbreviation is a list, types must also be a list of the same length."
                        )
                        items.extend(
                            [
                                ITagData(
                                    level=x,
                                    volume=v,
                                    abbreviation=a,
                                    type_reference=t,
                                    level_iref=i,
                                )
                                for a, t in zip(gen_def.abbreviation, gen_def.types, strict=False)
                            ],
                        )
                    else:
                        for a in gen_def.abbreviation:
                            items.extend(
                                [
                                    ITagData(
                                        level=x,
                                        volume=v,
                                        abbreviation=a,
                                        level_iref=i,
                                    ),
                                ],
                            )
                else:
                    items.extend([ITagData(level=x, volume=v, abbreviation=gen_def.abbreviation, level_iref=i)])

    return items


def batch_gen_idata(gen_defs: list[GenDefinition], config: ConfigIref | None = None) -> list[ITagData]:
    return list(chain(*[gen_idata(gen_def, config) for gen_def in gen_defs]))
