import os, sys
import archook

# Add arcpy's directories to sys.path
try:
    archook.get_arcpy(pro=True)
except ImportError:
    print('Unable to locate arcpy directory')

# Additional tweaks to placate arcpy
from types import ModuleType
sys.path.append('./site-packages')  # Add a dummy site-packages folder to sys.path
sys.modules['numpy'] = ModuleType('numpy')  # Add a fake numpy module to sys.modules
if not os.path.exists(os.path.join(sys.prefix, 'conda-meta')):
    os.mkdir(os.path.join(sys.prefix, 'conda-meta'))
