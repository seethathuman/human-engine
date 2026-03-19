#!/usr/bin/env python3
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import *
from PySide6.QtWebEngineWidgets import QWebEngineView

class WebView(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.web = QWebEngineView()
        self.web.load(QUrl("http://127.0.0.1:5337"))
        self.toolbar = None

        self.layout.addWidget(self.web)

    def set_toolbar(self, toolbar):
        self.toolbar = toolbar
        self.layout.addWidget(toolbar)

    def reload(self):
        self.parentWidget().raise_()
        self.web.reload()