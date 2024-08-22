from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import Qt

from ags_service_publisher.logging_io import setup_logger
from ags_service_publisher.services import normalize_services

from ..helpers.confighelpers import get_configs_cached
from ..helpers.pathhelpers import get_config_dir

log = setup_logger(__name__)


class ServiceSelector(QtWidgets.QWidget):

    selectionChanged = QtCore.pyqtSignal(tuple, tuple)

    (
        NAME,
        TYPE,
        CATEGORY,
    ) = range(3)

    def __init__(self, parent=None):
        super(ServiceSelector, self).__init__(parent)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.tab_widget = QtWidgets.QTabWidget(self)
        self.layout.addWidget(self.tab_widget)

        self.model = ServiceModel(0, 3, self)
        self.model.setHeaderData(self.NAME, Qt.Orientation.Horizontal, 'Name')
        self.model.setHeaderData(self.TYPE, Qt.Orientation.Horizontal, 'Type')
        self.model.setHeaderData(self.CATEGORY, Qt.Orientation.Horizontal, 'Category')

        configs = get_configs_cached(config_dir=get_config_dir())
        categories = []
        no_category_count = 0

        for config_name, config in configs.items():
            category = config.get('category')
            if category:
                if category not in categories:
                    categories.append(category)
            else:
                no_category_count += 1

            config_item = CheckableItem(config_name)
            config_item.setFlags(config_item.flags() | Qt.ItemFlag.ItemIsAutoTristate)

            services = config.get('services')
            default_service_properties = config.get('default_service_properties')
            for service_name, service_type, _ in normalize_services(services, default_service_properties):
                service_item = CheckableItem(service_name)
                config_item.appendRow((service_item, QtGui.QStandardItem(f'{service_type} Service'), QtGui.QStandardItem(category)))
            self.model.appendRow((config_item, QtGui.QStandardItem('Config Name'), QtGui.QStandardItem(category)))

        self.add_tab(self.model, 'All')

        for category in categories:
            proxy_model = QtCore.QSortFilterProxyModel(self)
            proxy_model.setSourceModel(self.model)
            proxy_model.setFilterKeyColumn(self.CATEGORY)
            proxy_model.setFilterFixedString(category)
            self.add_tab(proxy_model, category)

        if no_category_count > 0:
            proxy_model = NoCategoryFilterProxyModel(self)
            proxy_model.setSourceModel(self.model)
            proxy_model.category_column = self.CATEGORY
            self.add_tab(proxy_model, '(none)')

        self.model.checkedItemsChanged.connect(self.selected_items_changed)

    def add_tab(self, model, heading):
        tree_view = QtWidgets.QTreeView()
        tree_view.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        tree_view.setModel(model)
        tree_view.setAlternatingRowColors(True)
        tree_view.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        tree_view.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        tree_view.header().setMinimumSectionSize(100)
        tree_view.header().setStretchLastSection(False)
        tree_view.header().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tab_widget.addTab(tree_view, heading)

    def selected_items_changed(self):
        self.selectionChanged.emit(*map(tuple, self.get_selected_items()))

    def get_selected_items(self):
        log.debug('Getting selected items')
        included_configs = []
        included_services = []
        for i in range(self.model.rowCount()):
            config_item = self.model.item(i, self.NAME)
            if config_item.checkState() in (Qt.CheckState.Checked, Qt.CheckState.PartiallyChecked):
                config_name = str(config_item.text())
                included_configs.append(config_name)
                log.debug(f'Selected config name: {config_name}')
            for j in range(config_item.rowCount()):
                service_item = config_item.child(j, self.NAME)
                if service_item.checkState() == Qt.CheckState.Checked:
                    service_name = str(service_item.text())
                    included_services.append(service_name)
                    log.debug(f'Selected service name: {service_name}')
        return included_configs, included_services


class CheckableItem(QtGui.QStandardItem):
    def __init__(self, *args, **kwargs):
        super(CheckableItem, self).__init__(*args, **kwargs)
        self.setCheckable(True)

    def setData(self, value, role):
        state = self.checkState()
        super(CheckableItem, self).setData(value, role)
        if (
            role == Qt.ItemDataRole.CheckStateRole and
            state != self.checkState()
        ):
            model = self.model()
            if model is not None and model.itemChecked is not None:
                model.itemChecked.emit(self)


class ServiceModel(QtGui.QStandardItemModel):

    itemChecked = QtCore.pyqtSignal(CheckableItem)
    checkedItemsChanged = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(ServiceModel, self).__init__(*args, **kwargs)
        self.itemChecked.connect(self.handle_item_checked)

    def handle_item_checked(self, item):
        self.itemChecked.disconnect(self.handle_item_checked)
        checked = item.checkState()
        log.debug(f'Item {item.text()} {"checked" if checked in (Qt.CheckState.PartiallyChecked, Qt.CheckState.Checked) else "unchecked"}')
        parent = item.parent()
        if not parent:
            if checked != Qt.CheckState.PartiallyChecked:
                for i in range(item.rowCount()):
                    item.child(i).setCheckState(checked)
        else:
            checked_count = 0
            for i in range(parent.rowCount()):
                if parent.child(i).checkState() == Qt.CheckState.Checked:
                    checked_count += 1
            if checked_count == 0:
                parent.setCheckState(Qt.CheckState.Unchecked)
            elif checked_count == parent.rowCount():
                parent.setCheckState(Qt.CheckState.Checked)
            else:
                parent.setCheckState(Qt.CheckState.PartiallyChecked)
        self.itemChecked.connect(self.handle_item_checked)
        self.checkedItemsChanged.emit()


class NoCategoryFilterProxyModel(QtCore.QSortFilterProxyModel):
    def __init__(self, *args, **kwargs):
        super(NoCategoryFilterProxyModel, self).__init__(*args, **kwargs)
    
    def filterAcceptsRow(self, source_row, source_parent):
        if not source_parent.isValid():
            model = self.sourceModel()
            category_index = model.index(source_row, self.category_column, source_parent)
            category = model.data(category_index)
            return not category
        return True
