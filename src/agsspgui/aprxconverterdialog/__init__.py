from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt

from ags_service_publisher.logging_io import setup_logger
from ags_service_publisher.config_io import get_config

from .aprxconverterdialog_ui import Ui_APRXConverterDialog

from ..helpers.pathhelpers import get_config_dir

log = setup_logger(__name__)


class APRXConverterDialog(QtWidgets.QDialog, Ui_APRXConverterDialog):

    runConverter = QtCore.pyqtSignal(tuple, tuple, tuple)

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowMaximizeButtonHint | Qt.WindowType.WindowMinimizeButtonHint)
        self._acceptButton = self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self._acceptButton.setText('Run converter')

        self.envsTree.header().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.selected_configs = ()
        self.selected_services = ()

        user_config = get_config('userconfig', config_dir=get_config_dir())
        for env_name, env in user_config['environments'].items():
            env_item = QtWidgets.QTreeWidgetItem(self.envsTree)
            env_item.setText(0, env_name)
            env_item.setText(1, 'Environment')
            env_item.setCheckState(0, Qt.CheckState.Unchecked)

        self.update_accept_button_state()
        self.buttonBox.accepted.connect(self.run_converter_on_selected_items)
        self.serviceSelector.selectionChanged.connect(self.service_selector_selection_changed)
        self.envsTree.itemChanged.connect(self.update_accept_button_state)

    def service_selector_selection_changed(self, selected_configs, selected_services):
        self.selected_configs = selected_configs
        self.selected_services = selected_services
        self.update_accept_button_state()

    def update_accept_button_state(self):
        log.debug('Updating accept button state')
        included_configs, included_services, included_envs = self.get_selected_items()
        self._acceptButton.setEnabled(
            len(included_configs) > 0 and
            len(included_envs) > 0
        )

    def get_selected_items(self):
        log.debug('Getting selected items')
        included_envs = []
        envs_root = self.envsTree.invisibleRootItem()
        for i in range(envs_root.childCount()):
            env_item = envs_root.child(i)
            if env_item.checkState(0) == Qt.CheckState.Checked:
                env_name = str(env_item.text(0))
                included_envs.append(env_name)
                log.debug('Selected env name: {}'.format(env_name))
        return self.selected_configs, self.selected_services, included_envs

    def run_converter_on_selected_items(self):
        included_configs, included_services, included_envs = map(tuple, self.get_selected_items())
        self.runConverter.emit(included_configs, included_services, included_envs)
