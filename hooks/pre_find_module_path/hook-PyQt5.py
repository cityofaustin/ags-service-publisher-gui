import glob
import os

from PyInstaller.utils.hooks import logger


def pre_find_module_path(api):
    '''
    Hook to apply modifications to default PyQt5 hook that reduce the size
    of the built executable.
    '''
    from PyInstaller.utils.hooks import qt

    logger.info('Overriding get_qt_binaries in hooks/qt.py')
    qt.get_qt_binaries = get_qt_binaries

    logger.info('Excluding unused Qt dependencies')
    keys_to_delete = [key for key in qt._qt5_dynamic_dependencies_dict.keys() if key not in (
        'qt5core',
        'qt5gui',
        'qt5widgets',
    )]
    for key in keys_to_delete:
        del qt._qt5_dynamic_dependencies_dict[key]

    logger.info('Excluding unused Qt translations')
    for key, value in qt._qt5_dynamic_dependencies_dict.items():
        qt._qt5_dynamic_dependencies_dict[key] = tuple((
            element if index != 1 else None for index, element in enumerate(value)
        ))

    logger.info('Excluding unused Qt plugins')
    from PyInstaller.utils import misc
    misc.files_in_dir = files_in_dir


def get_qt_binaries(qt_library_info):
    # Monkey-patch that omits unused Qt binaries to reduce file size
    binaries = []
    return binaries


def files_in_dir(directory, file_patterns=[]):
    # Monkey-patch that excludes specific Qt plugins to reduce file size
    included_files = []
    excluded_files = []
    exclusion_patterns = [
        'qminimal.dll',
        'qoffscreen.dll',
        'qtvirtualkeyboardplugin.dll',
        'qwebgl.dll',
        'qxdgdesktopportal.dll',
    ]
    for file_pattern in file_patterns:
        included_files.extend(glob.glob(os.path.join(directory, file_pattern)))
    for file_pattern in exclusion_patterns:
        excluded_files.extend(glob.glob(os.path.join(directory, file_pattern)))
    files = list(set(included_files) - set(excluded_files))
    return files
