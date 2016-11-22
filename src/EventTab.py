# -*- coding: utf-8 -*-
"""
Tab for editing events.
"""

from PyQt5.QtCore import QVariant, pyqtSignal
from PyQt5.QtWidgets import QWidget, QTableView, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QAbstractItemView
from src.CheckBoxEdit import CheckBoxEdit
from src.DbModel import DbModel
from src.EventManager import EventManager
from src.ItemDelegateDateEdit import ItemDelegateDateEdit
from src.ItemDelegateSpinBoxEdit import ItemDelegateSpinBoxEdit
from src.Resources import Resources
from src.Tools import Tools


class EventTab(QWidget):
    """
    Widget which represents tab for editing events.
    """

    save_clicked_signal = pyqtSignal()

    def __init__(self, db: DbModel):
        super(EventTab, self).__init__()
        self.__manager = EventManager(db)
        self.__manager.model.select()
        self.__create_view()
        self.setLayout(self.__layout)

    def __create_view(self):
        self.__view = QTableView()
        self.__view.setModel(self.__manager.model)
        self.__view.setSelectionMode(QAbstractItemView.NoSelection)
        self.__layout = QVBoxLayout()
        self.__layout.addWidget(self.__view)
        self.__layout.addLayout(self.__create_buttons())
        self.__set_columns_delegate()
        self.__set_columns_checkbox([Resources.EventManager_Column_IsCyclic_Index, Resources.EventManager_Column_IsActive_Index])
        self.__set_columns_visible()
        self.__set_columns_width()
        self.__set_columns_title()

    def __set_columns_delegate(self):
        self.__delegate_start_date = ItemDelegateDateEdit()
        self.__delegate_number = ItemDelegateSpinBoxEdit(1)
        self.__delegate_days = ItemDelegateSpinBoxEdit()
        self.__delegate_months = ItemDelegateSpinBoxEdit()
        self.__view.setItemDelegateForColumn(2, self.__delegate_start_date)
        self.__view.setItemDelegateForColumn(4, self.__delegate_number)
        self.__view.setItemDelegateForColumn(5, self.__delegate_days)
        self.__view.setItemDelegateForColumn(6, self.__delegate_months)

    def __set_columns_checkbox(self, column_list: list):
        for column in column_list:
            for row in range(self.__manager.model.rowCount()):
                self.__set_column_checkbox(row, column)

    def __set_column_checkbox(self, row: int, column: int):
        index = self.__manager.model.index(row, column)
        check_box = CheckBoxEdit(None)
        check_box.set_property(Resources.EventTab_Property_Row, QVariant(row))
        check_box.set_property(Resources.EventTab_Property_Column, QVariant(column))
        check_box.state_changed.connect(self.__checkbox_clicked)
        check_box.checked = bool(index.data())
        self.__view.setIndexWidget(index, check_box)

    def __create_buttons(self):
        self.__add_button = self.__create_button(Resources.EventTab_BUTTON_NAME_Add, self.__add_clicked)
        self.__delete_button = self.__create_button(Resources.EventTab_BUTTON_NAME_Delete, self.__delete_clicked)
        self.__save_button = self.__create_button(Resources.EventTab_BUTTON_NAME_Save, self.__save_clicked)

        layout = QHBoxLayout()
        layout.addWidget(self.__add_button)
        layout.addWidget(self.__delete_button)
        layout.addStretch(1)
        layout.addWidget(self.__save_button)

        return layout

    def __create_button(self, name: str, fun: object):
        button = QPushButton(self)
        button.setText(name)
        button.clicked.connect(fun)

        return button

    def __set_columns_visible(self):
        for key, value in Resources.EventTab_Columns_Visible.items():
            self.__view.setColumnHidden(key, not value)

    def __set_columns_width(self):
        for key, value in Resources.EventTab_Columns_Width.items():
            self.__view.setColumnWidth(key, value)

    def __set_columns_title(self):
        for key, value in Resources.EventTab_Columns_Names.items():
            self.__manager.set_header_title(key, value)

    def __checkbox_clicked(self, state: int):
        del state
        sender = self.sender()
        row = int(sender.property(Resources.EventTab_Property_Row))
        column = int(sender.property(Resources.EventTab_Property_Column))
        index = self.__manager.model.index(row, column)
        self.__manager.model.setData(index, sender.isChecked())

    def __add_clicked(self):
        index = self.__manager.insert_row()
        self.__set_column_checkbox(index, Resources.EventManager_Column_IsCyclic_Index)
        self.__set_column_checkbox(index, Resources.EventManager_Column_IsActive_Index)

    def __delete_clicked(self):
        reply = QMessageBox.warning(self, Resources.EventTab_BUTTON_NAME_Delete, Resources.EventTab_Delete_Message, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.No:
            return

        selected_indexes = self.__view.selectedIndexes()
        self.__manager.remove_rows(selected_indexes)

    def __save_clicked(self):
        self.__manager.save()
        self.__set_columns_checkbox([Resources.EventManager_Column_IsCyclic_Index, Resources.EventManager_Column_IsActive_Index])
        self.save_clicked_signal.emit()
        Tools.write_verbose_class_name(self, "Save clicked")
