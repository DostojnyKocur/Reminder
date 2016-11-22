# -*- coding: utf-8 -*-
"""
Main application class.
"""

import os
from PyQt5.QtWidgets import QApplication
from src.Tools import Tools, Config, ExecutedType
from src.MainWindow import MainWindow


class Application:
    """
    Main application class.
    """

    @staticmethod
    def run(params: list) -> int:
        """
        Starts the application.
        :return: Error code. If no error occurred returns 0.
        """
        for item in params:
            if str(item).lower() == "--verbose":
                Config.set_executed_type(ExecutedType.Verbose)
                break

        result = -1
        try:
            exec_real_path = os.path.realpath(params[0])
            exec_dir = os.path.dirname(exec_real_path)
            Config.set_root_dir(exec_dir)

            app = QApplication(params)

            Tools.check_paths()

            window = MainWindow()
            window.show()

            result = app.exec_()
        except Exception as ex:  # wildcard for an app crash
            Tools.write_log(ex)
            result = -2
        finally:
            Tools.write_verbose("Application error code is %s" % result)

        return result
