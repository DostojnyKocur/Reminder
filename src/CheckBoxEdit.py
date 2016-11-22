# -*- coding: utf-8 -*-
"""
Checkbox widget.
"""

from PyQt5.QtWidgets import QWidget, QCheckBox, QHBoxLayout
from PyQt5.QtCore import Qt, QVariant
from src.Tools import Tools


class CheckBoxEdit(QWidget):
    """
    Widget with centered checkbox.
    """

    def __init__(self, parent):
        super(CheckBoxEdit, self).__init__(parent)
        self.__editor = QCheckBox(self)
        layout = QHBoxLayout(self)
        layout.addWidget(self.__editor, 0, Qt.AlignCenter)
        layout.setContentsMargins(1, 1, 1, 1)
        self.setAutoFillBackground(True)

    def set_property(self, name: str, value: QVariant):
        """
        Sets property.
        :param name: Property's name.
        :param value: New Value.
        """
        self.__editor.setProperty(name, value)
        Tools.write_verbose_class_method_name(self, CheckBoxEdit.set_property, name, str(value.value()))

    def get_property(self, name: str) -> QVariant:
        """
        Returns property's value.
        :param name: Property's name.
        :return: Value.
        """
        result = self.__editor.property(name)
        Tools.write_verbose_class_method_name(self, CheckBoxEdit.get_property, name, str(result))
        return result

    @property
    def enabled(self):
        """
        Returns whether editor is enabled.
        :return: True if editor is enabled, otherwise False.
        """
        result = self.__editor.isEnabled()
        Tools.write_verbose_class_method_name(self, "enabled", "get_enabled", str(result))
        return result

    @enabled.setter
    def enabled(self, value: bool):
        """
        Sets editor is enabled.
        :param value: New value.
        """
        self.__editor.setEnabled(value)
        Tools.write_verbose_class_method_name(self, "enabled", "set_enabled", str(value))

    @property
    def checked(self):
        """
        Returns whether editor is checked.
        :return: True if editor is checked, otherwise False.
        """
        result = self.__editor.isChecked()
        Tools.write_verbose_class_method_name(self, "checked", "get_checked", str(result))
        return result

    @checked.setter
    def checked(self, value: bool):
        """
        Sets editor is checked.
        :param value: New value.
        """
        self.__editor.setChecked(value)
        Tools.write_verbose_class_method_name(self, "checked", "set_checked", str(value))

    @property
    def state_changed(self):
        """
        Returns state changed signal.
        :return: Signal.
        """
        return self.__editor.stateChanged

