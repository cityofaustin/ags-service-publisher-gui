import functools

from ags_service_publisher.config_io import get_config, get_configs
from ags_service_publisher.logging_io import setup_logger

log = setup_logger(__name__)


@functools.lru_cache(maxsize=1)
def get_config_cached(*args, **kwargs):
    return get_config(*args, **kwargs)

@functools.lru_cache(maxsize=1)
def get_configs_cached(*args, **kwargs):
    return get_configs(*args, **kwargs)

def reload_configs(*args, **kwargs):
    get_config_cached.cache_clear()
    get_configs_cached.cache_clear()
    mode = kwargs.pop('mode', 'load')
    include_userconfig = kwargs.pop('include_userconfig', False)
    try:
        log.info(f'{mode.capitalize()}ing configuration files...')
        if include_userconfig:
            get_config_cached('userconfig', **kwargs)
        get_configs_cached(*args, **kwargs)
        log.info(f'Configuration files successfully {mode}ed.')
    except:
        log.exception(f'An error occurred {mode}ing configuration files')
