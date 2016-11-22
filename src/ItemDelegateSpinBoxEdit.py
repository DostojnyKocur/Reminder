# -*- coding: utf-8 -*-
"""
Abstract delegate providing a spin box editor.
"""

from PyQt5.QtWidgets import QStyledItemDelegate, QSpinBox, QWidget, QStyleOptionViewItem
from PyQt5.QtCore import QModelIndex, QAbstractItemModel, QVariant, QLocale
from src.Tools import Tools


class ItemDelegateSpinBoxEdit(QStyledItemDelegate):
    """
    Delegate class with SpinBox as an editor.
    """

    def __init__(self, minimum: int = 0):
        super(ItemDelegateSpinBoxEdit, self).__init__(None)
        self.__minimum = minimum

    def createEditor(self, parent: QWidget, options: QStyleOptionViewItem, index: QModelIndex) -> QSpinBox:
        """
        Creates an editor.
        :param parent: Parent widget.
        :param options: Options.
        :param index: Model's index.
        :return: Created editor.
        """
        editor = QSpinBox(parent)
        editor.setMinimum(self.__minimum)
        return editor

    def setEditorData(self, editor: QWidget, index: QModelIndex):
        """
        Sets data to an editor.
        :param editor: Editor.
        :param index: Model's index.
        """
        value = index.data()
        editor.setValue(value)
        Tools.write_verbose_class_method_name(self, ItemDelegateSpinBoxEdit.setEditorData, "value", str(value))

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex):
        """
        Sets data from editor back to model.
        :param editor: Editor.
        :param model: Model.
        :param index: Model's index.
        """
        value = editor.value()
        model.setData(index, value)
        Tools.write_verbose_class_method_name(self, ItemDelegateSpinBoxEdit.setModelData, "value", str(value))

    def displayText(self, value: QVariant, locale: QLocale) -> str:
        """
        Returns a text to display.
        :param value: Value to parse.
        :param locale: Locale format.
        :return: Text to display.
        """
        return str(value)
