# -*- coding: utf-8 -*-
"""
Main window.
"""

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QTabWidget
from src.Tools import Config
from src.DbModel import DbModel
from src.EventTab import EventTab
from src.ReminderEventTab import ReminderEventTab
from src.Resources import Resources


class MainWindow(QMainWindow):
    """
    Application main window.
    """

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowIcon(QIcon(Config.ICON_PATH))

        self.__db = DbModel(Config.DB_NAME)
        self.__tabs = QTabWidget()
        self.__add_tabs()

        super(MainWindow, self).setCentralWidget(self.__tabs)
        super(MainWindow, self).setFixedSize(Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)
        super(MainWindow, self).setWindowTitle(Config.WINDOW_TITLE)

    def __add_tabs(self):
        self.__reminder_event_tab = ReminderEventTab(self.__db)
        self.__event_tab = EventTab(self.__db)

        self.__event_tab.save_clicked_signal.connect(self.__reminder_event_tab.reload_slot)

        self.__tabs.addTab(self.__reminder_event_tab, Resources.TAB_NAME_Reminder)
        self.__tabs.addTab(self.__event_tab, Resources.TAB_NAME_Event)
