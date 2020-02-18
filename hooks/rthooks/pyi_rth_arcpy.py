import os
import sys
import archook

# Add arcpy's directories to sys.path
try:
    archook.get_arcpy(pro=True)
except ImportError:
    print('Unable to locate arcpy directory')

# Additional tweaks to placate arcpy
if not os.path.exists(os.path.join(sys.prefix, 'conda-meta')):
    os.mkdir(os.path.join(sys.prefix, 'conda-meta'))
