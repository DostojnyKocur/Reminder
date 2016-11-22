# -*- coding: utf-8 -*-
"""
Manager to operate on reminder data.
"""

from PyQt5.QtCore import QDateTime, QDate
from PyQt5.QtSql import QSqlQueryModel
from src.Tools import Tools
from src.DbModel import DbModel
from src.Resources import Resources


class ReminderManager:
    """
    Manager to manage remind logic.
    """

    def __init__(self, db: DbModel):
        self.__db = db
        self.__model = QSqlQueryModel()
        self.refresh_data()

    def set_done(self, reminder_id: int, event_id: int):
        """
        Sets flag IsDone on 1 for a given Id and adds next events to the reminder.
        :param reminder_id: Reminder event Id.
        :param event_id: Event Id.
        """
        self.__db.exec(Resources.ReminderManager_UPDATE_ReminderEventIsDone % str(reminder_id))
        self.__add_events_to_reminder(reminder_id, event_id)
        Tools.write_verbose_class_method_name(self, ReminderManager.set_done, "reminder_id", str(reminder_id))

    def refresh_data(self):
        """
        Repopulate model.
        """
        today_date = QDateTime().currentDateTime().toString(Resources.FORMAT_DATE_STORE)
        query = Resources.ReminderManager_SELECT_ReminderEventList % today_date
        self.model.setQuery(query)
        Tools.write_verbose_class_name(self, "Data refreshed for date %s" % today_date)
        Tools.write_verbose_class_method_name(self, ReminderManager.refresh_data, "query", query)

    def __add_events_to_reminder(self, index: int, event_id: int):
        event_info = self.__get_event_info(event_id)
        count_to_add = self.__get_event_count_to_add(event_info)
        Tools.write_verbose_class_method_name(self, ReminderManager.__add_events_to_reminder, "count_to_add", str(count_to_add))

        if count_to_add == 0:
            return

        start_date = self.__get_new_reminder_event_date(index, event_info)
        start_date = start_date.toString(Resources.FORMAT_DATE_STORE)

        for i in range(count_to_add):
            sql = Resources.Manager_INSERT_ReminderEvent % (event_id, start_date)
            self.__db.exec(sql)

    def __get_new_reminder_event_date(self, index: int, event_info: dict) -> QDate:
        day_count = int(event_info["Day"])
        month_count = int(event_info["Month"])
        reminder_date = self.__get_reminder_event_date(index)
        new_date = reminder_date.addMonths(month_count)
        new_date = new_date.addDays(day_count)

        return new_date

    def __get_event_count_to_add(self, event_info: dict) -> int:
        zero = 0
        if not bool(event_info["IsActive"]):
            return zero
        if not bool(event_info["IsCyclic"]):
            return zero
        start_date = Tools.get_date_from_string(str(event_info["StartDate"]))
        current_date = Tools.get_current_date()
        if start_date > current_date:
            return zero
        count_to_add = int(event_info["Count"]) - int(event_info["ReminderCount"])
        if count_to_add <= 0:
            return zero

        Tools.write_verbose_class_method_name(self, ReminderManager.__get_event_count_to_add, "count_to_add", str(count_to_add))
        return count_to_add

    def __get_event_info(self, event_id: int) -> dict:
        event_id_str = str(event_id)
        query = self.__db.exec(Resources.ReminderManager_SELECT_EventInfo % (event_id_str, event_id_str))
        query.next()
        result = {
            "StartDate": query.value(0),
            "IsCyclic": query.value(1),
            "Count": query.value(2),
            "Day": query.value(3),
            "Month": query.value(4),
            "IsActive": query.value(5),
            "ReminderCount": query.value(6)
        }

        return result

    def __get_reminder_event_date(self, index: int) -> QDate:
        query = self.__db.exec(Resources.ReminderManager_SELECT_ReminderEventDate % str(index))
        query.next()
        date = query.value(0)
        if not date:
            date = ''

        return Tools.get_date_from_string(date)

    @property
    def model(self):
        """
        Returns query model.
        :return: Query model.
        """
        return self.__model

