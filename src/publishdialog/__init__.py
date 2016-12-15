from PyQt4 import QtGui
from PyQt4.QtCore import Qt

from ags_service_publisher.logging_io import setup_logger
from ags_service_publisher.publisher import get_configs, normalize_services
from publishdialog import Ui_PublishDialog

log = setup_logger(__name__)


class PublishDialog(QtGui.QDialog, Ui_PublishDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        for config_name, config in get_configs().iteritems():
            services = config.get('services')
            default_service_properties = config.get('default_service_properties')
            config_item = QtGui.QTreeWidgetItem(self.treeWidget)
            config_item.setText(0, config_name)
            config_item.setText(1, 'Config Name')
            config_item.setFlags(config_item.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            for service_name, service_type, service_properties in normalize_services(services, default_service_properties):
                service_item = QtGui.QTreeWidgetItem(config_item)
                service_item.setText(0, service_name)
                service_item.setText(1, '{} Service'.format(service_type))
                service_item.setFlags(service_item.flags() | Qt.ItemIsUserCheckable)
                service_item.setCheckState(0, Qt.Unchecked)
        self.buttonBox.accepted.connect(self.publish_selected_items)

    def publish_selected_items(self):
        included_configs = []
        included_services = []
        root = self.treeWidget.invisibleRootItem()
        for i in range(root.childCount()):
            config_item = root.child(i)
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
        if len(included_configs) > 0:
            self.parent().publish_services(included_configs=included_configs, included_services=included_services)
