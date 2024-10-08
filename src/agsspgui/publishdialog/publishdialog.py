from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt

from ags_service_publisher.logging_io import setup_logger

from .publishdialog_ui import Ui_PublishDialog

from ..helpers.pathhelpers import get_config_dir
from ..helpers.confighelpers import get_config_cached

log = setup_logger(__name__)


class PublishDialog(QtWidgets.QDialog, Ui_PublishDialog):

    publishSelected = QtCore.pyqtSignal(tuple, tuple, tuple, tuple, bool, bool, bool, bool)

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.settings = QtCore.QSettings()

        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowMaximizeButtonHint | Qt.WindowType.WindowMinimizeButtonHint)
        self._acceptButton = self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self._acceptButton.setText('Publish selected services')

        self.instancesTree.header().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.selected_configs = ()
        self.selected_services = ()

        user_config = get_config_cached('userconfig', config_dir=get_config_dir())
        for env_name, env in user_config['environments'].items():
            env_item = QtWidgets.QTreeWidgetItem(self.instancesTree)
            env_item.setText(0, env_name)
            env_item.setText(1, 'Environment')
            env_item.setFlags(env_item.flags() | Qt.ItemFlag.ItemIsAutoTristate)
            for instance_name in env.get('ags_instances'):
                instance_item = QtWidgets.QTreeWidgetItem(env_item)
                instance_item.setText(0, instance_name)
                instance_item.setText(1, 'AGS Instance')
                instance_item.setCheckState(0, Qt.CheckState.Unchecked)

        self.update_publish_button_state()
        self.buttonBox.accepted.connect(self.publish_selected_items)
        self.serviceSelector.selectionChanged.connect(self.service_selector_selection_changed)
        self.instancesTree.itemChanged.connect(self.update_publish_button_state)
        QtCore.QTimer.singleShot(0, self.read_settings)
        self.finished.connect(self.write_settings)

    def write_settings(self):
        self.settings.beginGroup('WindowSettings/ModalDialogs')
        self.settings.setValue('geometry', self.saveGeometry())
        self.settings.setValue('splitterState', self.splitter.saveState())
        self.settings.endGroup()

    def read_settings(self):
        self.settings.beginGroup('WindowSettings/ModalDialogs')
        self.restoreGeometry(self.settings.value('geometry', QtCore.QByteArray()))
        self.splitter.restoreState(self.settings.value('splitterState', QtCore.QByteArray()))
        self.settings.endGroup()

    def service_selector_selection_changed(self, selected_configs, selected_services):
        self.selected_configs = selected_configs
        self.selected_services = selected_services
        self.update_publish_button_state()

    def update_publish_button_state(self):
        log.debug('Updating publish button state')
        included_configs, included_services, included_envs, included_instances, create_backups, copy_source_files_from_staging_folder, delete_existing_services, publish_services = self.get_selected_items()
        self._acceptButton.setEnabled(
            (len(included_configs) > 0 and len(included_instances) > 0)
        )

    def get_selected_items(self):
        log.debug('Getting selected items')
        included_envs = []
        included_instances = []
        instances_root = self.instancesTree.invisibleRootItem()
        for i in range(instances_root.childCount()):
            env_item = instances_root.child(i)
            if env_item.checkState(0) in (Qt.CheckState.Checked, Qt.CheckState.PartiallyChecked):
                env_name = str(env_item.text(0))
                included_envs.append(env_name)
                log.debug(f'Selected env name: {env_name}')
            for j in range(env_item.childCount()):
                instance_item = env_item.child(j)
                if instance_item.checkState(0) == Qt.CheckState.Checked:
                    instance_name = str(instance_item.text(0))
                    included_instances.append(instance_name)
                    log.debug(f'Selected instance name: {instance_name}')
        create_backups = self.createBackupsCheckBox.isChecked()
        copy_source_files_from_staging_folder = self.copyStagingFilesCheckBox.isChecked()
        delete_existing_services = self.deleteExistingServicesCheckBox.isChecked()
        publish_services = self.publishServicesCheckBox.isChecked()
        return self.selected_configs, self.selected_services, included_envs, included_instances, create_backups, copy_source_files_from_staging_folder, delete_existing_services, publish_services

    def publish_selected_items(self):
        included_configs, included_services, included_envs, included_instances, create_backups, copy_source_files_from_staging_folder, delete_existing_services, publish_services = self.get_selected_items()
        self.publishSelected.emit(
            tuple(included_configs),
            tuple(included_services),
            tuple(included_envs),
            tuple(included_instances),
            create_backups,
            copy_source_files_from_staging_folder,
            delete_existing_services,
            publish_services,
        )
