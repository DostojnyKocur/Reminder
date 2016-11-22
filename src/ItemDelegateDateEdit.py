# -*- coding: utf-8 -*-
"""
Abstract delegate providing a date editor.
"""

from PyQt5.QtWidgets import QStyledItemDelegate, QDateEdit, QWidget, QStyleOptionViewItem
from PyQt5.QtCore import QModelIndex, QAbstractItemModel, QVariant, QLocale
from src.Tools import Tools
from src.Resources import Resources


class ItemDelegateDateEdit(QStyledItemDelegate):
    """
    Delegate class with DateEdit as an editor.
    """

    def __init__(self):
        super(ItemDelegateDateEdit, self).__init__(None)
        self.__minimum = {}

    def createEditor(self, parent: QWidget, options: QStyleOptionViewItem, index: QModelIndex) -> QDateEdit:
        """
        Creates an editor.
        :param parent: Parent widget.
        :param options: Options.
        :param index: Model's index.
        :return: Created editor.
        """
        editor = QDateEdit(parent)
        editor.setDisplayFormat(Resources.FORMAT_DATE_DISPLAY)
        return editor

    def setEditorData(self, editor: QWidget, index: QModelIndex):
        """
        Sets data to an editor.
        :param editor: Editor.
        :param index: Model's index.
        """
        date = Tools.get_date_from_string(str(index.data()))
        row = index.row()

        if row not in self.__minimum:
            self.__minimum[row] = date

        editor.setMinimumDate(self.__minimum[row])
        editor.setDate(date)
        Tools.write_verbose_class_method_name(self, ItemDelegateDateEdit.setEditorData, "date", str(date))

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex):
        """
        Sets data from editor back to model.
        :param editor: Editor.
        :param model: Model.
        :param index: Model's index.
        """
        date = editor.date().toString(Resources.FORMAT_DATE_STORE)
        model.setData(index, date)
        Tools.write_verbose_class_method_name(self, ItemDelegateDateEdit.setModelData, "date", str(date))

    def displayText(self, value: QVariant, locale: QLocale) -> str:
        """
        Returns a text to display.
        :param value: Value to parse.
        :param locale: Locale format.
        :return: Text to display.
        """
        date = Tools.get_date_from_string(str(value))
        return date.toString(Resources.FORMAT_DATE_DISPLAY)
