import os, sys


def get_app_path():
    return sys.executable if getattr(sys, 'frozen', False) else os.path.realpath(sys.argv[0])
