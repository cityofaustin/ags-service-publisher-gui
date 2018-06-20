from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Qt

from ags_service_publisher.logging_io import setup_logger
from ags_service_publisher.config_io import get_config, get_configs
from ags_service_publisher.services import normalize_services
from publishdialog_ui import Ui_PublishDialog

log = setup_logger(__name__)


class PublishDialog(QtWidgets.QDialog, Ui_PublishDialog):

    publishSelected = QtCore.Signal(tuple, tuple, tuple, tuple)

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint | Qt.WindowMinimizeButtonHint)
        self._acceptButton = self.buttonBox.addButton('Publish selected services', QtWidgets.QDialogButtonBox.AcceptRole)

        self.servicesTree.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.instancesTree.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        for config_name, config in get_configs(config_dir=parent.config_dir).iteritems():
            services = config.get('services')
            config_item = QtWidgets.QTreeWidgetItem(self.servicesTree)
            config_item.setText(0, config_name)
            config_item.setText(1, 'Config Name')
            config_item.setFlags(config_item.flags() | Qt.ItemIsTristate)
            for service_name, service_type, _ in normalize_services(services):
                service_item = QtWidgets.QTreeWidgetItem(config_item)
                service_item.setText(0, service_name)
                service_item.setText(1, '{} Service'.format(service_type))
                service_item.setCheckState(0, Qt.Unchecked)
        user_config = get_config('userconfig', config_dir=parent.config_dir)
        for env_name, env in user_config['environments'].iteritems():
            env_item = QtWidgets.QTreeWidgetItem(self.instancesTree)
            env_item.setText(0, env_name)
            env_item.setText(1, 'Environment')
            env_item.setFlags(env_item.flags() | Qt.ItemIsTristate)
            for instance_name in env.get('ags_instances'):
                instance_item = QtWidgets.QTreeWidgetItem(env_item)
                instance_item.setText(0, instance_name)
                instance_item.setText(1, 'AGS Instance')
                instance_item.setCheckState(0, Qt.Unchecked)
        self.update_publish_button_state()

        self.buttonBox.accepted.connect(self.publish_selected_items)
        self.servicesTree.itemChanged.connect(self.update_publish_button_state)
        self.instancesTree.itemChanged.connect(self.update_publish_button_state)

    def update_publish_button_state(self):
        log.debug('Updating publish button state')
        included_configs, included_services, included_envs, included_instances = self.get_selected_items()
        self._acceptButton.setEnabled(
            (len(included_configs) > 0 and len(included_instances) > 0)
        )

    def get_selected_items(self):
        log.debug('Getting selected items')
        included_configs = []
        included_services = []
        included_envs = []
        included_instances = []
        services_root = self.servicesTree.invisibleRootItem()
        for i in range(services_root.childCount()):
            config_item = services_root.child(i)
            if config_item.checkState(0) in (Qt.Checked, Qt.PartiallyChecked):
                config_name = str(config_item.text(0))
                included_configs.append(config_name)
                log.debug('Selected config name: {}'.format(config_name))
            for j in range(config_item.childCount()):
                service_item = config_item.child(j)
                if service_item.checkState(0) == Qt.Checked:
                    service_name = str(service_item.text(0))
                    included_services.append(service_name)
                    log.debug('Selected service name: {}'.format(service_name))
        instances_root = self.instancesTree.invisibleRootItem()
        for i in range(instances_root.childCount()):
            env_item = instances_root.child(i)
            if env_item.checkState(0) in (Qt.Checked, Qt.PartiallyChecked):
                env_name = str(env_item.text(0))
                included_envs.append(env_name)
                log.debug('Selected env name: {}'.format(env_name))
            for j in range(env_item.childCount()):
                instance_item = env_item.child(j)
                if instance_item.checkState(0) == Qt.Checked:
                    instance_name = str(instance_item.text(0))
                    included_instances.append(instance_name)
                    log.debug('Selected instance name: {}'.format(instance_name))
        return map(tuple, (included_configs, included_services, included_envs, included_instances))

    def publish_selected_items(self):
        self.publishSelected.emit(*self.get_selected_items())
