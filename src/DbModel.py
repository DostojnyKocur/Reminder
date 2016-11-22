# -*- coding: utf-8 -*-
"""
Class which represents database model.
Provides methods to access and manipulate on a data.
"""

from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from src.Tools import Tools, Config
from src.Resources import Resources


class DbModel:
    """
    Class which represents model of the database.
    """

    def __init__(self, name: str):
        self.__db_path = Config.DB_PATH + name
        self.__init_db()

    def __del__(self):
        self.__db.close()

    def exec(self, query_string: str) -> QSqlQuery:
        """
        Executes query.
        :param query_string: Query to execute.
        :return: Executed query.
        """
        query = self.__get_query()
        Tools.write_verbose(query_string)
        query.exec(query_string)
        Tools.write_log(query.lastError().text())

        return query

    def __init_db(self):
        self.__db = QSqlDatabase.addDatabase(Config.DB_TYPE)
        self.db.setDatabaseName(self.__db_path)

        if not self.db.isValid():
            Tools.write_log(self.db.lastError().text())
        if self.db.isOpenError():
            Tools.write_log(self.db.lastError().text())

        self.db.open()
        tables = self.db.tables()

        if not tables:
            self.__create_db()

    def __create_db(self):
        Tools.write_log("Creating tables...")
        self.exec(Resources.CREATE_TABLE_Event)
        self.exec(Resources.CREATE_TABLE_ReminderEvent)
        Tools.write_log("Done.")

    def __get_query(self) -> QSqlQuery:
        return QSqlQuery(self.db)

    @property
    def db(self):
        """
        Returns database object.
        :return: Database object.
        """
        return self.__db


