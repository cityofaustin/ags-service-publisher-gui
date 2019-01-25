# ArcGIS Server Service Publisher GUI

**Note: This is a work in progress!**

## Overview

This is the graphical user interface (GUI) application for the [ArcGIS Server Service Publisher](https://github.com/cityofaustin/ags-service-publisher) Python library.

It currently enables users to publish services to ArcGIS Server and run a number of different report types.

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

TODO

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
