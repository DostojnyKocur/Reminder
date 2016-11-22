# -*- coding: utf-8 -*-
"""
Hardcoded resources.
"""

from PyQt5.QtCore import QDate


class Resources:
    """
    Class to store resources.
    """

    FORMAT_DATE_DISPLAY = "dd-MM-yyyy"
    FORMAT_DATE_STORE = "yyyyMMdd"
    TABLE_NAME_Reminder = "ReminderEvent"
    TABLE_NAME_Event = "Event"
    TAB_NAME_Reminder = "Reminders"
    TAB_NAME_Event = "Event list"

    CREATE_TABLE_Event = """
        CREATE TABLE Event
        (
            Id INTEGER PRIMARY KEY,
            Name VARCHAR,
            StartDate VARCHAR,
            IsCyclic INTEGER,
            Count INTEGER,
            Day INTEGER,
            Month INTEGER,
            IsActive INTEGER
        )
        """
    CREATE_TABLE_ReminderEvent = """
        CREATE TABLE ReminderEvent
        (
            Id INTEGER PRIMARY KEY,
            EventId INTEGER,
            Date VARCHAR,
            IsDone INTEGER
        )
        """

    ReminderEventTab_Columns_Visible = {
        0: False,
        1: False,
        2: False,
        3: True,
        4: True
    }
    ReminderEventTab_Columns_Width = {
        0: 100,
        1: 100,
        2: 100,
        3: 630,
        4: 100
    }
    ReminderEventTab_Columns_Names = {
        0: "Id",
        1: "EventId",
        2: "Date",
        3: "Title",
        4: ""
    }
    ReminderEventTab_Column_EventId = 1
    ReminderEventTab_BUTTON_NAME_Done = "Done"
    ReminderEventTab_Property_Id = "propId"
    ReminderEventTab_Property_EventId = "propEventId"

    ReminderManager_SELECT_ReminderEventList = """
        SELECT
            R.Id,
            R.EventId,
            R.Date,
            E.Name
        FROM
            ReminderEvent AS R
            INNER JOIN Event AS E ON R.EventId=E.Id
        WHERE
            E.IsActive=1
            AND R.IsDone=0
            AND R.Date<='%s'
        ORDER BY
            E.Name
        """
    ReminderManager_SELECT_ReminderEventDate = """
        SELECT
            Date
        FROM
            ReminderEvent
        WHERE
            Id=%s
        """
    ReminderManager_UPDATE_ReminderEventIsDone = """
        UPDATE ReminderEvent SET IsDone=1 WHERE IsDone=0 AND Id=%s
        """
    ReminderManager_SELECT_EventInfo = """
        SELECT
            StartDate,
            IsCyclic,
            Count,
            Day,
            Month,
            IsActive,
            (SELECT COUNT(*) FROM ReminderEvent WHERE EventId=%s AND IsDone=0) AS ReminderCount
        FROM
            Event
        WHERE
            Id=%s
    """

    EventTab_BUTTON_NAME_Add = "Add"
    EventTab_BUTTON_NAME_Delete = "Delete"
    EventTab_BUTTON_NAME_Save = "Save"
    EventTab_Delete_Message = "Do you want to delete selected events and all their reminders?"
    EventTab_Columns_Visible = {
        0: False,
        1: True,
        2: True,
        3: True,
        4: True,
        5: True,
        6: True,
        7: True
    }
    EventTab_Columns_Width = {
        0: 100,
        1: 390,
        2: 90,
        3: 55,
        4: 55,
        5: 55,
        6: 55,
        7: 55
    }
    EventTab_Columns_Names = {
            0: "Id",
            1: "Title",
            2: "Start Date",
            3: "Cyclic",
            4: "Number",
            5: "Days",
            6: "Months",
            7: "Active"
        }
    EventTab_Property_Row = "propRow"
    EventTab_Property_Column = "propColumn"

    EventManager_Columns_Default_Values = {
        1: "ENTER TITLE HERE",
        2: QDate().currentDate().toString(FORMAT_DATE_STORE),
        3: 1,
        4: 1,
        5: 0,
        6: 0,
        7: 1
    }
    EventManager_Column_Title_Index = 1
    EventManager_Column_StartDate_Index = 2
    EventManager_Column_IsCyclic_Index = 3
    EventManager_Column_Count_Index = 4
    EventManager_Column_Day_Index = 5
    EventManager_Column_Month_Index = 6
    EventManager_Column_IsActive_Index = 7
    EventManager_SELECT_MaxId = """
        SELECT MAX(Id) FROM """ + TABLE_NAME_Event
    EventManager_SELECT_Event = """
        SELECT
            Id,
            Name,
            StartDate,
            IsCyclic,
            Count,
            Day,
            Month,
            IsActive
        FROM
            Event """ + TABLE_NAME_Event + """
        WHERE
            Id=%s
    """
    EventManager_DELETE_Newest_ReminderEvents = """
        DELETE FROM """ + TABLE_NAME_Reminder + """
        WHERE Id IN
        (
            SELECT Id FROM """ + TABLE_NAME_Reminder + """
            WHERE IsDone=0 AND EventId=%s
            ORDER BY Id DESC LIMIT %s
        ) """
    EventManager_DELETE_Event = """
        DELETE FROM """ + TABLE_NAME_Event + """
        WHERE Id=%s
        """
    EventManager_DELETE_ReminderEvent = """
        DELETE FROM """ + TABLE_NAME_Reminder + """
        WHERE EventId=%s
        """

    Manager_INSERT_ReminderEvent = """
        INSERT INTO """ + TABLE_NAME_Reminder + """
        (EventId, Date, IsDone) VALUES (%s, %s, 0) """
    Manager_DELETE_ReminderEvent = """
        DELETE FROM """ + TABLE_NAME_Reminder + """
        WHERE IsDone=0 AND EventId=%s"""

    # verbose section
    Verbose_Class_Method_Name = "[control = %s] [method = %s] (name = %s) (value = %s)"
    Verbose_Class_Name = "[control = %s] %s"






