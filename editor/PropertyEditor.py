#!/usr/bin/env python3
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

class PropertyEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QFormLayout(self)
        self.layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft)
        self.current_item = None

    def open(self, data):
        self.parentWidget().raise_()
        if data == self.current_item:
            return
        for _ in range(self.layout.rowCount()):
            self.layout.removeRow(0)
        for field, value in data.items():
            widget = None
            match field:
                case _:
                    if isinstance(value, str):
                        widget = PropertyEdit(field, data)
            if widget:
                self.layout.addRow(field, widget)

class PropertyEdit(QLineEdit):
    def __init__(self, field, data):
        super().__init__()
        self.field = field
        self.data = data
        self.setText(data[field])
        self.setPlaceholderText(field)
        self.editingFinished.connect(self.save_edit)

    def save_edit(self):
        self.data[self.field] = self.text()
        print(f"EDIT: {self.data}")
