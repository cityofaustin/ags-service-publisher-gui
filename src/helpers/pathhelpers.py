import os, sys, inspect

import ags_service_publisher


def get_app_path():
    return sys.executable if getattr(sys, 'frozen', False) else os.path.realpath(sys.argv[0])


def get_lib_path():
    return sys.executable if getattr(sys, 'frozen', False) else os.path.realpath(os.path.dirname(inspect.getfile(ags_service_publisher)))
