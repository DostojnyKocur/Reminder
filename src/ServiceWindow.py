# -*- coding: utf-8 -*-
"""
Test window.
"""

from PyQt5.QtWidgets import QWidget, QTableView, QVBoxLayout
from PyQt5.QtCore import QAbstractTableModel


class ServiceWindow(QWidget):
    """
    Window for service purposes.
    """
    def __init__(self, model: QAbstractTableModel, window_title: str):
        super(ServiceWindow, self).__init__()
        self.__model = model

        self.__view = QTableView()
        self.__view.setModel(self.__model)
        self.__layout = QVBoxLayout()
        self.__layout.addWidget(self.__view)

        super(ServiceWindow, self).setWindowTitle(window_title)
        super(ServiceWindow, self).setLayout(self.__layout)
