# -*- coding: utf-8 -*-
"""
Tab for events to remind.
"""

from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtSql import QSqlRecord
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QAbstractItemView
from src.DbModel import DbModel
from src.ReminderManager import ReminderManager
from src.Resources import Resources
from src.Tools import Tools


class ReminderEventTab(QWidget):
    """
    Widget which represents tab for events to remind.
    """

    def __init__(self, db: DbModel):
        super(ReminderEventTab, self).__init__()
        self.__manager = ReminderManager(db)
        self.__create_view()
        self.setLayout(self.__layout)

    def reload_slot(self):
        """
        Reloads view's content.
        """
        self.__view.clearContents()
        self.__manager.refresh_data()
        self.__fill_content()
        self.__set_header_titles(Resources.ReminderEventTab_Columns_Names)
        Tools.write_verbose_class_name(self, "View reloaded")

    def __create_view(self):
        self.__view = QTableWidget()
        self.__view.setSelectionMode(QAbstractItemView.NoSelection)
        self.__layout = QVBoxLayout()
        self.__layout.addWidget(self.__view)
        self.__fill_content()
        self.__set_header_titles(Resources.ReminderEventTab_Columns_Names)

    def __fill_content(self):
        rows = self.__manager.model.rowCount()
        self.__prepare_view(rows, len(Resources.ReminderEventTab_Columns_Names))
        self.__set_column_visible()
        self.__set_columns_width()

        for i in range(0, rows):
            self.__add_row_to_widget(i)

    def __add_row_to_widget(self, index: int):
        record = self.__manager.model.record(index)
        self.__add_value_to_row(record, index, 0, "Id")
        self.__add_value_to_row(record, index, 1, "EventId")
        self.__add_value_to_row(record, index, 2, "Date")
        self.__add_value_to_row(record, index, 3, "Name")
        self.__add_button_to_row(record, index, 4)

    def __add_button_to_row(self, record: QSqlRecord, row: int, column: int):
        button = QPushButton(Resources.ReminderEventTab_BUTTON_NAME_Done)
        button.setProperty(Resources.ReminderEventTab_Property_Id, QVariant(record.value(0)))
        button.setProperty(Resources.ReminderEventTab_Property_EventId, QVariant(record.value(Resources.ReminderEventTab_Column_EventId)))
        button.clicked.connect(self.__button_clicked)
        self.__view.setCellWidget(row, column, button)

    def __button_clicked(self):
        sender = self.sender()
        index = int(sender.property(Resources.ReminderEventTab_Property_Id))
        event_id = int(sender.property(Resources.ReminderEventTab_Property_EventId))
        self.__manager.set_done(index, event_id)
        Tools.write_verbose_class_method_name(self, ReminderEventTab.__button_clicked, "index", str(index))
        self.__remove_row(index)

    def __remove_row(self, index: int):
        row = -1
        # looking for row's number in view for given reminder id
        for row_number in range(self.__view.rowCount()):
            item = int(self.__view.item(row_number, 0).text())
            if item == index:
                row = row_number
                break

        self.__view.removeRow(row)
        Tools.write_verbose_class_method_name(self, ReminderEventTab.__remove_row, "__view.removeRow", str(row))

    def __prepare_view(self, row_count: int, column_count: int):
        self.__view.setRowCount(row_count)
        self.__view.setColumnCount(column_count)

    def __set_header_titles(self, column_header_dict: dict):
        for key, value in column_header_dict.items():
            self.__view.setHorizontalHeaderItem(key, QTableWidgetItem(value))

    def __set_column_visible(self):
        for key, value in Resources.ReminderEventTab_Columns_Visible.items():
            if not value:
                self.__view.hideColumn(key)

    def __set_columns_width(self):
        for key, value in Resources.ReminderEventTab_Columns_Width.items():
            self.__view.setColumnWidth(key, value)

    def __add_value_to_row(self, record: QSqlRecord, row: int, column: int, value_name: str, is_editable: bool = False, is_selectable: bool = True, is_enable: bool = True):
        item = QTableWidgetItem(str(record.value(value_name)))
        flags = item.flags()

        if is_editable:
            flags = flags | Qt.ItemIsEditable
        else:
            flags = flags & ~Qt.ItemIsEditable

        if is_selectable:
            flags = flags | Qt.ItemIsSelectable
        else:
            flags = flags & ~Qt.ItemIsSelectable

        if is_enable:
            flags = flags | Qt.ItemIsEnabled
        else:
            flags = flags & ~Qt.ItemIsEnabled

        item.setFlags(flags)
        self.__view.setItem(row, column, item)
