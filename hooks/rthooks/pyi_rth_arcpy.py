import sys

# Add arcpy's directories to sys.path
from archook import get_arcpy
try:
    get_arcpy()
except ImportError:
    print 'Unable to locate arcpy directory'

# Additional tweaks to placate arcpy
from types import ModuleType
sys.path.append('./site-packages')  # Add a dummy site-packages folder to sys.path
sys.modules['numpy'] = ModuleType('numpy')  # Add a fake numpy module to sys.modules
