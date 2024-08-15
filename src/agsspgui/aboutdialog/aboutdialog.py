from pkg_resources import get_distribution
from PyQt6 import QtWidgets

from .aboutdialog_ui import Ui_AboutDialog


class AboutDialog(QtWidgets.QDialog, Ui_AboutDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.textBrowser.setHtml(
            self.textBrowser.toHtml().replace(
                '{ags_service_publisher_gui_version}',
                str(get_distribution('ags_service_publisher_gui').version)
            ).replace(
                '{ags_service_publisher_library_version}',
                str(get_distribution('ags_service_publisher').version)
            )
        )
