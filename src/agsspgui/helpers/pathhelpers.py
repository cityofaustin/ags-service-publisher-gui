import os, sys, inspect

import ags_service_publisher


def get_app_path():
    return sys.executable if getattr(sys, 'frozen', False) else os.path.realpath(sys.argv[0])


def get_lib_path():
    return sys.executable if getattr(sys, 'frozen', False) else os.path.realpath(os.path.dirname(inspect.getfile(ags_service_publisher)))


def get_config_dir():
    return os.getenv(
        'AGS_SERVICE_PUBLISHER_CONFIG_DIR',
        os.path.abspath(os.path.join(os.path.dirname(get_lib_path()), 'configs'))
    )


def get_log_dir():
    return os.getenv(
        'AGS_SERVICE_PUBLISHER_LOG_DIR',
        os.path.abspath(os.path.join(os.path.dirname(get_lib_path()), 'logs'))
    )


def get_report_dir():
    return os.getenv(
        'AGS_SERVICE_PUBLISHER_REPORT_DIR',
        os.path.abspath(os.path.join(os.path.dirname(get_lib_path()), 'reports'))
    )
