# -*- coding: utf-8 -*-
"""
Library to store and access configuration and log.
"""

from enum import Enum
from PyQt5.QtCore import QDir, QDateTime, QFile, QTextStream, QDate
from src.Resources import Resources


class ExecutedType(Enum):
    """
    Class to describe type of an app execution.
    """
    Silent = 1
    """
    Silent type writes to log only information about errors.
    """
    Verbose = 2
    """
    Verbose type writes to log all information about app work.
    """


class Config:
    """
    Config consts.
    """
    EXECUTED_TYPE = ExecutedType.Silent
    ROOT_DIR = ""
    ICON_PATH = "icon.png"
    LOG_PATH = "log/"
    DB_PATH = "db/"
    DB_NAME = "maindb"
    DB_TYPE = "QSQLITE"
    WINDOW_HEIGHT = 600
    WINDOW_WIDTH = 800
    WINDOW_TITLE = "Reminder"

    @staticmethod
    def set_root_dir(new_dir: str):
        """
        Sets the root path of executing script.
        :param new_dir: New root path.
        """
        if new_dir[-1] != '/':
            new_dir += '/'

        Config.ROOT_DIR = new_dir
        Config.ICON_PATH = Config.ROOT_DIR + Config.ICON_PATH
        Config.LOG_PATH = Config.ROOT_DIR + Config.LOG_PATH
        Config.DB_PATH = Config.ROOT_DIR + Config.DB_PATH

    @staticmethod
    def set_executed_type(new_type: ExecutedType):
        """
        Sets executed type for the app.
        :param new_type: New type.
        """
        Config.EXECUTED_TYPE = new_type


class Tools:
    """
    Class with useful methods.
    """

    @staticmethod
    def is_verbose() -> bool:
        """
        Returns whether current executed type is verbose.
        :return: True if current executed type is verbose, False otherwise.
        """
        return Config.EXECUTED_TYPE == ExecutedType.Verbose

    @staticmethod
    def check_path(path: str):
        """
        Checks if path exists. If not, creates one.
        :param path: Path to check.
        """
        check_dir = QDir(path)
        if not check_dir.exists():
            if Tools.is_verbose():
                print("Not exists '%s'." % path)
            if not check_dir.mkpath(".") and Tools.is_verbose():
                print("Could not create '%s'" % path)
            elif Tools.is_verbose():
                print("Created '%s'" % path)
        elif Tools.is_verbose():
            print("Exists '%s'." % path)

    @staticmethod
    def check_paths():
        """
        Checks all Config paths. Creates path if not exists.
        """
        Tools.check_path(Config.DB_PATH)
        Tools.check_path(Config.LOG_PATH)

    @staticmethod
    def write_verbose_class_name(instance: object, message: str):
        """
        Writes verbose message. Message started from class name.
        :param instance: Class instance.
        :param message: Message to write.
        :return:
        """
        new_message = Resources.Verbose_Class_Name % (instance.__class__.__name__, message)
        Tools.write_verbose(new_message)

    @staticmethod
    def write_verbose_class_method_name(instance: object, method: object, name: str, value: str):
        """
        Writes verbose message for setter method.
        :param instance: Class instance.
        :param method: Caller method.
        :param name: Property name.
        :param value: Property value.
        """
        if isinstance(method, str):
            method_name = method
        else:
            method_name = str(method.__name__)

        Tools.write_verbose(Resources.Verbose_Class_Method_Name % (instance.__class__.__name__, method_name, name, value))

    @staticmethod
    def write_verbose(message):
        """
        If the app is executed in verbose mode writes message to current log file and prints it on the output.
        If the app is executed in silent mode does nothing.
        :param message: Message to write.
        """
        if not Tools.is_verbose():
            return

        end_message = Tools.prepare_message_string(message)
        Tools.write_to_log_file(end_message)
        print(end_message)

    @staticmethod
    def write_log(message):
        """
        Writes message to current log file.
        If message is empty does nothing.
        If the app is executed in verbose mode prints the message on the output.
        :param message: Message to write.
        """

        end_message = Tools.prepare_message_string(message)

        if not end_message:
            return

        Tools.write_to_log_file(end_message)

        if Tools.is_verbose():
            print(end_message)

    @staticmethod
    def get_date_from_string(string: str) -> QDate:
        """
        Returns date from given string.
        Uses FORMAT_DATE_STORE.
        :param string: String to convert.
        :return: Date.
        """
        return QDate.fromString(string, Resources.FORMAT_DATE_STORE)

    @staticmethod
    def get_current_date() -> QDate:
        """
        Returns current date.
        :return: Current date.
        """
        current_date = QDate()
        return current_date.currentDate()

    @staticmethod
    def prepare_message_string(message) -> str:
        """
        Prepares string message from given parameter.
        :param message: Given message.
        :return: String message.
        """
        result = ""

        if message:
            message_str = "%s" % message

            if len(message_str.strip()) > 0:
                result = QDateTime().currentDateTime().toString("HH:mm:ss") + ': ' + message_str + "\n"

        return result

    @staticmethod
    def write_to_log_file(message: str):
        """
        Writes given message to current log file.
        :param message: Message to write.
        """
        log_path = Config.LOG_PATH + "log_" + QDateTime().currentDateTime().toString("yyyy_MM_dd") + ".log"
        current_file = QFile(log_path)
        try:
            current_file.open(QFile.WriteOnly | QFile.Append)
            stream = QTextStream(current_file)
            stream << message
        finally:
            current_file.close()
