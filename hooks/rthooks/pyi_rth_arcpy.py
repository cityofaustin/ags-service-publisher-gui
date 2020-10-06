import logging
import os
import sys

from ags_service_publisher.logging_io import setup_logger, setup_console_log_handler

log = setup_logger(__name__)
setup_console_log_handler(logging.root, verbose=True)

# Create conda-meta directory
conda_meta_dir = os.path.join(sys.prefix, 'conda-meta')
if not os.path.exists(conda_meta_dir):
    log.debug(f'creating conda-meta dir {conda_meta_dir}')
    os.mkdir(conda_meta_dir)
else:
    log.debug(f'conda-meta dir {conda_meta_dir} already exists')

# Add arcpy's directories to sys.path
try:
    log.debug('Importing archook')
    import archook
    log.debug('Running archook.get_arcpy')
    archook.get_arcpy(pro=True)
except ImportError:
    log.warning('Unable to locate arcpy directory')
