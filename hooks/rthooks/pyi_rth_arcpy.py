import os, sys

# Add arcpy's directories to sys.path
try:
    os.environ['PATH'] = ';'.join((r'C:\Program Files\ArcGIS\Pro\bin', os.environ['PATH']))
    sys.path.append(r'C:\Program Files\ArcGIS\Pro\bin')
    sys.path.append(r'C:\Program Files\ArcGIS\Pro\Resources\ArcPy')
    sys.path.append(r'C:\Program Files\ArcGIS\Pro\Resources\ArcToolbox\Scripts')
    sys.path.append(r'C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\Lib\site-packages')
except ImportError:
    print 'Unable to locate arcpy directory'

# Additional tweaks to placate arcpy
from types import ModuleType
sys.path.append('./site-packages')  # Add a dummy site-packages folder to sys.path
sys.modules['numpy'] = ModuleType('numpy')  # Add a fake numpy module to sys.modules
