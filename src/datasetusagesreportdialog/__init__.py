from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

from ags_service_publisher.logging_io import setup_logger
from ags_service_publisher.config_io import get_config
from ags_service_publisher.helpers import empty_tuple

from datasetusagesreportdialog_ui import Ui_DatasetUsagesReportDialog

from helpers.pathhelpers import get_config_dir

log = setup_logger(__name__)


class DatasetUsagesReportDialog(QtGui.QDialog, Ui_DatasetUsagesReportDialog):

    runReport = QtCore.pyqtSignal(tuple, tuple, tuple, str)

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint | Qt.WindowMinimizeButtonHint)
        self._acceptButton = self.buttonBox.button(QtGui.QDialogButtonBox.Ok)
        self._acceptButton.setText('Run report')

        self.instancesTree.header().setResizeMode(0, QtGui.QHeaderView.Stretch)

        user_config = get_config('userconfig', config_dir=get_config_dir())
        for env_name, env in user_config['environments'].iteritems():
            env_item = QtGui.QTreeWidgetItem(self.instancesTree)
            env_item.setText(0, env_name)
            env_item.setText(1, 'Environment')
            env_item.setFlags(env_item.flags() | Qt.ItemIsTristate)
            for instance_name in env.get('ags_instances'):
                instance_item = QtGui.QTreeWidgetItem(env_item)
                instance_item.setText(0, instance_name)
                instance_item.setText(1, 'AGS Instance')
                instance_item.setCheckState(0, Qt.Unchecked)

        self.update_accept_button_state()
        self.outputfileButton.clicked.connect(self.select_output_filename)
        self.buttonBox.accepted.connect(self.run_report_on_selected_items)
        self.instancesTree.itemChanged.connect(self.update_accept_button_state)

    def update_accept_button_state(self):
        log.debug('Updating accept button state')
        included_datasets, included_envs, included_instances = self.get_selected_items()
        self._acceptButton.setEnabled(
            len(included_instances) > 0
        )

    def get_selected_items(self):
        log.debug('Getting selected items')
        included_datasets_text = self.includedDatasetsTextEdit.toPlainText()
        included_datasets = included_datasets_text.split('\n') if included_datasets_text else empty_tuple
        included_envs = []
        included_instances = []
        instances_root = self.instancesTree.invisibleRootItem()
        for included_dataset in included_datasets:
            log.debug('Included dataset: {}'.format(included_dataset))
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
        return included_datasets, included_envs, included_instances

    def run_report_on_selected_items(self):
        included_datasets, included_envs, included_instances = map(tuple, self.get_selected_items())
        self.runReport.emit(included_datasets, included_envs, included_instances, self.outputfileLineEdit.text() or None)

    def select_output_filename(self):
        filename = QtGui.QFileDialog.getSaveFileName(
            self,
            'Output filename',
            self.outputfileLineEdit.text(),
            'Comma-separated value (CSV) files (*.csv)'
        )
        self.outputfileLineEdit.setText(filename)
        self.update_accept_button_state()
