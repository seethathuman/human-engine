#!/usr/bin/env python

import os.path
from PySide6.QtWidgets import *

class FileTabs(QTabWidget):
    def __init__(self):
        super().__init__()

        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)
        self.open_files = {}

    def open(self, path):
        self.parentWidget().raise_()
        if path in self.open_files:
            self.setCurrentWidget(self.open_files[path])
            return

        editor = QPlainTextEdit()

        with open(path, "r", encoding="utf8") as f:
            editor.setPlainText(f.read())

        name = os.path.basename(path)

        self.addTab(editor, name)
        self.setCurrentWidget(editor)

        self.open_files[path] = editor

    def close_tab(self, index):
        widget = self.widget(index)

        for k, v in list(self.open_files.items()):
            if v == widget:
                del self.open_files[k]

        self.removeTab(index)