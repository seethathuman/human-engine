#!/usr/bin/env python

import os.path
from PySide6.QtWidgets import *
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

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

        try:
            with open(path, "r", encoding="utf8") as f:
                data = f.read()
        except UnicodeDecodeError:
            with open(path, "rb") as f:
                data = f.read()

        if isinstance(data, str):
            editor = QPlainTextEdit()
            editor.setPlainText(data)
        else:
            pixmap = QPixmap(path)
            if not pixmap.isNull():
                editor = ImageView(pixmap)
            else:
                editor = QPlainTextEdit()
                editor.setPlainText(str(data))
                editor.setEnabled(False)

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

class ImageView(QLabel):
    def __init__(self, pixmap):
        super().__init__()
        self.orig_pixmap = pixmap
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(1, 1)

    def resizeEvent(self, event):
        scaled = self.orig_pixmap.scaled(
            self.contentsRect().size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.setPixmap(scaled)