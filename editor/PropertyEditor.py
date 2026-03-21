#!/usr/bin/env python3
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon

class PropertyEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout(self)

        self.form_layout = QFormLayout()
        self.form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        self.form_layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft)
        self.current_item = None
        self.main_layout.addLayout(self.form_layout)

        self.style_editor = None

    def open(self, data):
        self.parentWidget().raise_()
        if data == self.current_item: return
        for _ in range(self.form_layout.rowCount()): self.form_layout.removeRow(0)

        # setup fields
        widget = QLabel(data["type"])
        self.form_layout.addRow("element", widget)

        widget = PropertyEdit("name", data)
        self.form_layout.addRow("name", widget)

        widget = PropertyEdit("id", data)
        self.form_layout.addRow("id", widget)

        widget = PropertyEdit("class", data)
        self.form_layout.addRow("class", widget)

        match data["type"]:
            case "img":
                widget = PropertyEdit("src-path", data)
                self.form_layout.addRow("image", widget)

        # if no child objects, enable content editing
        if not data["content"]: data["content"] = ""
        if isinstance(data["content"], str):
            widget = PropertyEdit("content", data)
            self.form_layout.addRow("content", widget)

        # initialize styles
        if not data["properties"].get("style", {}):
            data["properties"]["style"] = {}

        if not self.style_editor:
            self.style_editor = StylesEditor({})
            self.main_layout.addWidget(self.style_editor)

        self.style_editor.data = data["properties"]["style"]
        self.style_editor.populate()

class StylesEditor(QWidget):
    def __init__(self, styles):
        super().__init__()
        self.data = styles
        self.layout = QVBoxLayout(self)

        self.top_bar = QHBoxLayout()
        self.styles_label = QLabel("styles")
        self.top_bar.addWidget(self.styles_label)

        top_spacer = QSpacerItem(10, 0, QSizePolicy.Expanding)
        self.top_bar.addItem(top_spacer)

        self.new_entry = QLineEdit()
        self.new_entry.setPlaceholderText("field name")
        self.top_bar.addWidget(self.new_entry)

        self.new_action = QAction("&New", self)
        self.new_action.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd))
        self.new_action.setStatusTip("Add a new css style to the object.")
        self.new_action.triggered.connect(self._new_style)
        self.new_button = QToolButton()
        self.new_button.setDefaultAction(self.new_action)
        self.top_bar.addWidget(self.new_button)

        self.delete_action = QAction("&Delete", self)
        self.delete_action.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListRemove))
        self.delete_action.setStatusTip("Delete a css style from the object.")
        self.delete_action.triggered.connect(self._delete_style)
        self.delete_button = QToolButton()
        self.delete_button.setDefaultAction(self.delete_action)
        self.top_bar.addWidget(self.delete_button)

        self.layout.addLayout(self.top_bar)

        self.scroll_widget = QWidget()
        self.form_layout = QFormLayout(self.scroll_widget)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)

        self.layout.addWidget(self.scroll_area)
        self.fields = {}
        self.values = {}
        self.delete_mode = False

        self.layout.setContentsMargins(0, 0, 0, 0)

    def populate(self):
        self.delete_mode = False
        for _ in range(self.form_layout.rowCount()): self.form_layout.removeRow(0)
        self.fields, self.values = {}, {}
        for field, value in self.data.items():
            field_widget = StyleField(field)
            value_widget = StyleEntry(field, self.data)
            field_widget.set_delete(self._finish_delete)
            self.fields[field] = field_widget
            self.values[value] = value_widget
            self.form_layout.addRow(field_widget, value_widget)

    def _delete_style(self):
        if self.delete_mode:
            self._finish_delete()
            return
        self.delete_mode = True
        for field_widget in self.fields.values():
            field_widget.delete_button.show()

    def _finish_delete(self, field = None):
        self.delete_mode = False
        if field:
            self.data.pop(field)
        self.populate()

    def _new_style(self):
        field = self.new_entry.text()
        if not field: return
        self.new_entry.setText("")
        self.data[field] = ""
        self.populate()

class StyleEntry(QLineEdit):
    def __init__(self, field, data):
        super().__init__()
        self.data = data
        self.field = field
        self.setText(data[field])
        self.editingFinished.connect(self._finish)

    def _finish(self):
        self.data[self.field] = self.text()

class StyleField(QWidget):
    def __init__(self, field):
        super().__init__()
        self.field = field

        self.layout = QHBoxLayout(self)

        self.delete_action = QAction("&Delete", self)
        self.delete_action.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditDelete))
        self.delete_action.setStatusTip("Remove this css style from the object.")
        self.delete_action.triggered.connect(self._delete)
        self.delete_button = QToolButton()
        self.delete_button.setDefaultAction(self.delete_action)
        self.layout.addWidget(self.delete_button)

        self.field_label = QLabel(self.field)
        self.layout.addWidget(self.field_label)

        self.layout.setContentsMargins(0, 0, 0, 0)

        self.delete_button.hide()
        self.delete_callback = None

    def _delete(self):
        self.delete_callback(self.field)

    def set_delete(self, callback):
        self.delete_callback = callback

class PropertyEdit(QLineEdit):
    def __init__(self, field, data):
        super().__init__()
        self.field = field
        self.data = data
        self.setText(data.get(field, ""))
        self.editingFinished.connect(self._save_edit)
        self._save_edit()

    def _save_edit(self):
        self.data[self.field] = self.text()
