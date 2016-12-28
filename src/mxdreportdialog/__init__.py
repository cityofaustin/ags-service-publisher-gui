from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

from ags_service_publisher.logging_io import setup_logger
from ags_service_publisher.publisher import get_config, get_configs, normalize_services
from mxdreportdialog import Ui_MXDReportDialog

log = setup_logger(__name__)


class MXDReportDialog(QtGui.QDialog, Ui_MXDReportDialog):

    runReport = QtCore.pyqtSignal(tuple, tuple, tuple, str)

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint | Qt.WindowMinimizeButtonHint)
        self._acceptButton = self.buttonBox.addButton('Run report', QtGui.QDialogButtonBox.AcceptRole)

        self.servicesTree.header().setResizeMode(0, QtGui.QHeaderView.Stretch)
        self.envsTree.header().setResizeMode(0, QtGui.QHeaderView.Stretch)

        self.filename = ''

        for config_name, config in get_configs().iteritems():
            services = config.get('services')
            default_service_properties = config.get('default_service_properties')
            config_item = QtGui.QTreeWidgetItem(self.servicesTree)
            config_item.setText(0, config_name)
            config_item.setText(1, 'Config Name')
            config_item.setFlags(config_item.flags() | Qt.ItemIsTristate)
            for service_name, service_type, service_properties in normalize_services(services, default_service_properties):
                service_item = QtGui.QTreeWidgetItem(config_item)
                service_item.setText(0, service_name)
                service_item.setText(1, '{} Service'.format(service_type))
                service_item.setCheckState(0, Qt.Unchecked)
        user_config = get_config('userconfig')
        for env_name, env in user_config['environments'].iteritems():
            env_item = QtGui.QTreeWidgetItem(self.envsTree)
            env_item.setText(0, env_name)
            env_item.setText(1, 'Environment')
            env_item.setCheckState(0, Qt.Unchecked)
        self.update_accept_button_state()

        self.outputfileButton.clicked.connect(self.select_output_filename)
        self.buttonBox.accepted.connect(self.run_report_on_selected_items)
        self.servicesTree.itemChanged.connect(self.update_accept_button_state)
        self.envsTree.itemChanged.connect(self.update_accept_button_state)
        self.outputfileLineEdit.textEdited.connect(self.update_accept_button_state)

    def update_accept_button_state(self):
        log.debug('Updating accept button state')
        included_configs, included_services, included_envs = self.get_selected_items()
        self.filename = self.outputfileLineEdit.text()
        self._acceptButton.setEnabled(
            (len(included_configs) > 0 and len(included_envs) > 0)
            and len(self.filename) > 0
        )

    def get_selected_items(self):
        log.debug('Getting selected items')
        included_configs = []
        included_services = []
        included_envs = []
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
        envs_root = self.envsTree.invisibleRootItem()
        for i in range(envs_root.childCount()):
            env_item = envs_root.child(i)
            if env_item.checkState(0) == Qt.Checked:
                env_name = str(env_item.text(0))
                included_envs.append(env_name)
                log.debug('Selected env name: {}'.format(env_name))
        return map(tuple, (included_configs, included_services, included_envs))

    def run_report_on_selected_items(self):
        included_configs, included_services, included_envs = self.get_selected_items()
        self.runReport.emit(included_configs, included_services, included_envs, self.filename)

    def select_output_filename(self):
        self.filename = QtGui.QFileDialog.getSaveFileName(
            self,
            'Output filename', self.filename,
            'Comma-separated value (CSV) files (*.csv)'
        )
        self.outputfileLineEdit.setText(self.filename)
        self.update_accept_button_state()
