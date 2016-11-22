# -*- coding: utf-8 -*-
"""
Manager to operate on event data.
"""

from PyQt5.QtCore import Qt, QVariant, QModelIndex
from PyQt5.QtSql import QSqlTableModel, QSqlRecord
from src.DbModel import DbModel
from src.Resources import Resources
from src.Tools import Tools


class EventManager:
    """
    Manager to manage event logic.
    """

    def __init__(self, db: DbModel):
        self.__db = db
        self.__model = QSqlTableModel(None, self.__db.db)
        self.model.setTable(Resources.TABLE_NAME_Event)
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.beforeInsert.connect(self.__before_insert)
        self.model.beforeUpdate.connect(self.__before_update)
        self.model.beforeDelete.connect(self.__before_delete)
        self.__last_id = self.__get_last_id()
        self.__added_items = []

    def insert_row(self) -> int:
        """
        Inserts empty row to model.
        :return: Row's index in table.
        """
        rows_count = self.model.rowCount()
        new_record = self.__get_new_record()
        self.model.insertRecord(rows_count, new_record)
        Tools.write_verbose_class_name(self, "Row inserted at position %s" % rows_count)
        return rows_count

    def remove_rows(self, selected_indexes: list):
        """
        Delete selected rows.
        :param selected_indexes Selected rows' indexes.
        """
        for item in selected_indexes:
            self.__remove_row(item)
            Tools.write_verbose_class_name(self, "Row with id = %s removed" % item)

    def save(self):
        """
        Saves changes.
        """
        self.model.submitAll()
        Tools.write_verbose_class_name(self, "Model saved")

    def set_header_title(self, column: int, title: str):
        """
        Sets title for a column.
        :param column: Column's index.
        :param title: Column's title.
        """
        self.model.setHeaderData(column, Qt.Horizontal, title)

    def __before_insert(self, record: QSqlRecord):
        index = record.value(0)
        self.__insert_reminder_events(record)
        self.__added_items.remove(index)
        Tools.write_verbose_class_method_name(self, EventManager.__before_insert, "added_items.remove", str(index))
        Tools.write_verbose_class_method_name(self, EventManager.__before_insert, "added_items.remained", str(self.__added_items))

    def __before_update(self, row: int, record: QSqlRecord):
        del row
        index = record.value(0)
        query = self.__db.exec(Resources.EventManager_SELECT_Event % index)
        query.next()
        old_record = query.record()
        self.__update_active(old_record, record)
        self.__update_count(old_record, record)
        Tools.write_verbose_class_method_name(self, EventManager.__before_update, "updated", str(index))

    def __before_delete(self, row: int):
        record = self.model.record(row)
        index = record.value(0)
        self.__db.exec(Resources.EventManager_DELETE_ReminderEvent % index)
        self.__db.exec(Resources.EventManager_DELETE_Event % index)
        Tools.write_verbose_class_method_name(self, EventManager.__before_delete, "deleted", str(index))

    def __remove_row(self, item: QModelIndex):
        row_number = item.row()
        record = self.model.record(row_number)
        index = record.value(0)

        self.model.removeRow(row_number)
        if index in self.__added_items:  # the row was not saved in the database
            self.__added_items.remove(index)
            Tools.write_verbose_class_method_name(self, EventManager.__remove_row, "added_items.remove", str(index))
            Tools.write_verbose_class_method_name(self, EventManager.__remove_row, "added_items.remained", str(self.__added_items))

    def __get_new_record(self) -> QSqlRecord:
        record = self.model.record()
        self.__set_next_id(record)
        for key, value in Resources.EventManager_Columns_Default_Values.items():
            record.setValue(key, QVariant(value))

        return record

    def __set_next_id(self, record: QSqlRecord):
        if self.__added_items:
            new_id = self.__added_items[-1] + 1
        else:  # list is empty
            new_id = self.__last_id + 1

        record.setValue(0, QVariant(new_id))
        self.__added_items.append(new_id)
        self.__last_id = new_id
        Tools.write_verbose_class_method_name(self, EventManager.__set_next_id, "new_id", str(new_id))

    def __get_last_id(self) -> int:
        query = self.__db.exec(Resources.EventManager_SELECT_MaxId)
        query.next()
        index = query.value(0)
        if not index:
            index = 0

        Tools.write_verbose_class_method_name(self, EventManager.__get_last_id, "last_id", str(index))
        return int(index)

    def __insert_reminder_events(self, record: QSqlRecord):
        index = record.value(0)
        start_date = record.value(Resources.EventManager_Column_StartDate_Index)
        count = record.value(Resources.EventManager_Column_Count_Index)
        Tools.write_verbose_class_method_name(self, EventManager.__insert_reminder_events, "event_id", str(index))
        self.__insert_missing_reminder_events(index, start_date, count)

    def __insert_missing_reminder_events(self, event_id: int, start_date: str, count: int):
        for i in range(count):
            sql = Resources.Manager_INSERT_ReminderEvent % (event_id, start_date)
            self.__db.exec(sql)

    def __update_active(self, old_record: QSqlRecord, new_record: QSqlRecord):
        new_value = bool(new_record.value(Resources.EventManager_Column_IsActive_Index))
        if bool(old_record.value(Resources.EventManager_Column_IsActive_Index)) == new_value:
            return

        index = old_record.value(0)
        Tools.write_verbose_class_method_name(self, EventManager.__update_active, "event_id", str(index))

        if new_value is False:  # if change to inactive
            sql = Resources.Manager_DELETE_ReminderEvent % index
            self.__db.exec(sql)
        else:  # if change to active
            self.__insert_reminder_events(new_record)

    def __update_count(self, old_record: QSqlRecord, new_record: QSqlRecord):
        new_value = new_record.value(Resources.EventManager_Column_Count_Index)
        old_value = old_record.value(Resources.EventManager_Column_Count_Index)
        if new_value == old_value:
            return

        index = new_record.value(0)
        Tools.write_verbose_class_method_name(self, EventManager.__update_count, "event_id", str(index))

        if new_value > old_value:  # we need to add missing records
            start_date = new_record.value(Resources.EventManager_Column_StartDate_Index)
            count = new_value - old_value
            self.__insert_missing_reminder_events(index, start_date, count)
        else:  # we need to delete redundant records
            count = old_value - new_value
            sql = Resources.EventManager_DELETE_Newest_ReminderEvents % (index, count)
            self.__db.exec(sql)

    @property
    def model(self):
        """
        Returns table model.
        :return: Table model.
        """
        return self.__model
