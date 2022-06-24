# ArcGIS Server Service Publisher GUI

**Note: This is a work in progress!**

## Overview

This is the graphical user interface (GUI) application for the [ArcGIS Server Service Publisher](https://github.com/cityofaustin/ags-service-publisher) Python library.

It currently enables users to publish services to ArcGIS Server and run a number of different [report types](https://github.com/cityofaustin/ags-service-publisher#generate-reports).

## Screenshots

<img src="https://user-images.githubusercontent.com/8584785/52435434-7cb3bc80-2ad7-11e9-8720-6c43ecfe87ad.png" width="23%"></img> <img src="https://user-images.githubusercontent.com/8584785/52435442-7faead00-2ad7-11e9-98cd-318db72abc33.png" width="23%"></img> <img src="https://user-images.githubusercontent.com/8584785/52435657-fcda2200-2ad7-11e9-9f32-43969281b6ae.png" width="23%"></img> <img src="https://user-images.githubusercontent.com/8584785/58494154-1318f600-813a-11e9-9a2f-c3068f4cc9ee.png" width="23%"></img> 

## Requirements

- Windows 10 64-bit
- ArcGIS Pro 2.9.x
- Python 3.7.x

## Installation

1. Download the `ags_service_publisher_gui_pro.exe` executable from the [Releases](https://github.com/cityofaustin/ags-service-publisher-gui/releases) tab to a directory of your choice
2. Configure the application as described in the [Configuration section](https://github.com/cityofaustin/ags-service-publisher#configuration) of the `ags-service-publisher` README.

## Tips

- You can use [`fnmatch`][1]-style wildcards in the Included Datasets input box on the Dataset Usages Report interface. For example entering `CouncilDistrict*` would match both the `CouncilDistrictMap` and `CouncilDistrictsFill` services.
- The following environment variables are recognized:
    - `AGS_SERVICE_PUBLISHER_CONFIG_DIR`: Allows you to override which directory is used for your configuration files. Defaults to the
      `configs` directory beneath the executable's directory.
    - `AGS_SERVICE_PUBLISHER_LOG_DIR`: Allows you to override which directory is used for storing log files. Defaults to the `logs`
        directory beneath the executable's directory.
    - `AGS_SERVICE_PUBLISHER_REPORT_DIR`: Allows you to override which directory is used for writing reports. Default to the `reports` directory beneath the executable's directory.
- By default, backups are created when publishing MapServer, ImageServer and GeocodeServer services. A `Backups` subdirectory is created in the same directory as the source file(s), and a copy of the existing source files corresponding to the services to be published are placed there with a timestamp appended. To disable creating backups, uncheck the "Create backups" checkbox on the Publish Services dialog.

## Building

1. (Optional) Create and activate a [virtual environment](https://docs.python.org/3/library/venv.html) using the Python executable installed in the default ArcGIS Pro `conda` environment, e.g.:

    ```
    %PROGRAMFILES%\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe -m venv <venv name>
    <venv name>\Scripts\activate.bat
    ```
1. Install the [`ags-service-publisher`](https://github.com/cityofaustin/ags-service-publisher) library per its [instructions](https://github.com/cityofaustin/ags-service-publisher#installation)
2. Use pip to install the other development dependencies, e.g. `pip install -r requirements.txt`
3. Run the `build.bat` script. If successful, this will output an executable to the `dist` subdirectory.

## TODO

- Add interfaces for the other report types
- ~~Implement SSL support~~ Implemented in [`ags-service-publisher/#1`](https://github.com/cityofaustin/ags-service-publisher/pull/1)
- Expose prefix/suffix service name options
- Add a progress/results interface in addition to the log window
- Add filtering and searching in the log window
- Add a config file editor/generator
- Create interface for generating AGS tokens
- Create interface for batch importing SDE connection files
- ~~Add ArcGIS Pro support~~ Implemented in [`ags-service-publisher/#3`](https://github.com/cityofaustin/ags-service-publisher/pull/3)
- Probably lots of other stuff!

## License

As a work of the City of Austin, this project is in the public domain within the United States.

Additionally, we waive copyright and related rights in the work worldwide through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).

[1]: https://docs.python.org/2/library/fnmatch.html
