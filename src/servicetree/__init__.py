from collections import OrderedDict
from itertools import islice

from PySide2 import QtWidgets, QtCore

from ags_service_publisher.logging_io import setup_logger
from ags_service_publisher.config_io import get_configs
from ags_service_publisher.services import normalize_services

from helpers.pathhelpers import get_config_dir

log = setup_logger(__name__)


class ServiceTree(QtWidgets.QWidget):

    selectionChanged = QtCore.Signal(tuple, tuple)

    def __init__(self, parent=None):
        super(ServiceTree, self).__init__(parent)

        self.verticalLayout = QtWidgets.QVBoxLayout()

        self.tabBar = QtWidgets.QTabBar()
        self.tabBar.setAutoHide(True)

        self.verticalLayout.addWidget(self.tabBar)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.treeWidget = QtWidgets.QTreeWidget()
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.treeWidget.setColumnCount(2)
        self.treeWidget.header().setMinimumSectionSize(100)
        self.treeWidget.header().setStretchLastSection(False)
        self.treeWidget.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.treeWidget.headerItem().setText(0, 'Name')
        self.treeWidget.headerItem().setText(1, 'Type')

        self.verticalLayout.addWidget(self.treeWidget)

        self.setLayout(self.verticalLayout)

        self.configs = OrderedDict()
        self.categories = OrderedDict((
            (None, []),
        ))

        for config_name, config in get_configs(config_dir=get_config_dir()).iteritems():
            self.configs[config_name] = config
            category = config.get('category')
            if category in self.categories:
                self.categories[category].append(config_name)
            else:
                self.categories[category] = [config_name]

        for category, config_names in self.categories.iteritems():
            self.tabBar.addTab(category if category else 'Default')

        self.tab_selected(self.tabBar.currentIndex())
        self.tabBar.currentChanged.connect(self.tab_selected)

    def tab_selected(self, tab_index):
        if self.treeWidget.receivers(QtCore.SIGNAL('itemChanged(QTreeWidgetItem*,int)')) > 0:
            self.treeWidget.itemChanged.disconnect()
        if self.treeWidget.topLevelItemCount() > 0:
            self.treeWidget.clear()
        if tab_index >= 0:
            category, config_names = next(islice(self.categories.iteritems(), tab_index, None))
            for config_name, config in self.configs.iteritems():
                if config.get('category') == category:
                    services = config.get('services')
                    config_item = QtWidgets.QTreeWidgetItem(self.treeWidget)
                    config_item.setText(0, config_name)
                    config_item.setText(1, 'Config Name')
                    config_item.setFlags(config_item.flags() | QtCore.Qt.ItemIsTristate)
                    for service_name, service_type, _ in normalize_services(services):
                        service_item = QtWidgets.QTreeWidgetItem(config_item)
                        service_item.setText(0, service_name)
                        service_item.setText(1, '{} Service'.format(service_type))
                        service_item.setCheckState(0, QtCore.Qt.Unchecked)
        self.selected_items_changed()
        self.treeWidget.itemChanged.connect(self.selected_items_changed)

    def selected_items_changed(self):
        self.selectionChanged.emit(*self.get_selected_items())

    def get_selected_items(self):
        log.debug('Getting selected items')
        included_configs = []
        included_services = []
        services_root = self.treeWidget.invisibleRootItem()
        for i in range(services_root.childCount()):
            config_item = services_root.child(i)
            if config_item.checkState(0) in (QtCore.Qt.Checked, QtCore.Qt.PartiallyChecked):
                config_name = str(config_item.text(0))
                included_configs.append(config_name)
                log.debug('Selected config name: {}'.format(config_name))
            for j in range(config_item.childCount()):
                service_item = config_item.child(j)
                if service_item.checkState(0) == QtCore.Qt.Checked:
                    service_name = str(service_item.text(0))
                    included_services.append(service_name)
                    log.debug('Selected service name: {}'.format(service_name))
        return map(tuple, (included_configs, included_services))
