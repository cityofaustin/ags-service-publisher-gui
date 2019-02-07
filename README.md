# ArcGIS Server Service Publisher GUI

**Note: This is a work in progress!**

## Overview

This is the graphical user interface (GUI) application for the [ArcGIS Server Service Publisher](https://github.com/cityofaustin/ags-service-publisher) Python library.

It currently enables users to publish services to ArcGIS Server and run a number of different [report types](https://github.com/cityofaustin/ags-service-publisher#generate-reports).

## Screenshots

<img src="https://user-images.githubusercontent.com/8584785/52435434-7cb3bc80-2ad7-11e9-8720-6c43ecfe87ad.png" width="23%"></img> <img src="https://user-images.githubusercontent.com/8584785/52435442-7faead00-2ad7-11e9-98cd-318db72abc33.png" width="23%"></img> <img src="https://user-images.githubusercontent.com/8584785/52435657-fcda2200-2ad7-11e9-9f32-43969281b6ae.png" width="23%"></img> <img src="https://user-images.githubusercontent.com/8584785/52435669-01063f80-2ad8-11e9-9cde-bb0f465adab9.png" width="23%"></img> 

## Requirements

- Windows 7+
- ArcGIS Desktop 10.3+
- Python 2.7+

## Installation

1. Download the `ags_service_publisher_gui.exe` executable from the Releases tab to a directory of your choice
2. Configure the application as described in the [Configuration section](https://github.com/cityofaustin/ags-service-publisher#configuration) of the `ags-service-publisher` README.

## Tips

- You can use [`fnmatch`][1]-style wildcards in the Included Datasets input box on the Dataset Usages Report interface. For example entering `CouncilDistrict*` would match both the `CouncilDistrictMap` and `CouncilDistrictsFill` services.
- The following environment variables are recognized:
    - `AGS_SERVICE_PUBLISHER_CONFIG_DIR`: Allows you to override which directory is used for your configuration files. Defaults to the
      `configs` directory beneath the executable's directory.
    - `AGS_SERVICE_PUBLISHER_LOG_DIR`: Allows you to override which directory is used for storing log files. Defaults to the `logs`
        directory beneath the executable's directory.
    - `AGS_SERVICE_PUBLISHER_REPORT_DIR`: Allows you to override which directory is used for writing reports. Default to the `reports` directory beneath the executable's directory.

## Building

1. Download PyQt4 (`PyQt4‑4.11.4‑cp27‑cp27m‑win32.whl`) from this page: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4
2. Use pip to install the downloaded wheel, e.g. `pip install PyQt4‑4.11.4‑cp27‑cp27m‑win32.whl`
3. Add the PyQt4 directory, e.g. `<Python interpreter directory>\Lib\site-packages\PyQt4`, to your `PATH` environment variable, so that `pyuic4.bat` is available.
4. Install the [`ags-service-publisher`](https://github.com/cityofaustin/ags-service-publisher) library per its [instructions](https://github.com/cityofaustin/ags-service-publisher#installation)
5. Use pip to install the other development dependencies, e.g. `pip install -R requirements.txt`
6. Run the `build.bat` script. If successful, this will output an executable to the `dist` subdirectory.

## TODO

- Add interfaces for the other report types
- ~~Implement SSL support~~ Implemented in [`ags-service-publisher/#1`](https://github.com/cityofaustin/ags-service-publisher/pull/1)
- Expose prefix/suffix service name options
- Add a progress/results interface in addition to the log window
- Add filtering and searching in the log window
- Add a config file editor/generator
- Create interface for generating AGS tokens
- Create interface for batch importing SDE connection files
- Add ArcGIS Pro support
- Probably lots of other stuff!

## License

As a work of the City of Austin, this project is in the public domain within the United States.

Additionally, we waive copyright and related rights in the work worldwide through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).

[1]: https://docs.python.org/2/library/fnmatch.html
