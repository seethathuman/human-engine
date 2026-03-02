#!/usr/bin/env python3

from project import Project
import server
import sys
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView

app = QApplication(sys.argv)
class Editor(QWidget):
    def __init__(self, project: Project):
        super().__init__()
        self.setWindowTitle("Human Engine Project Editor")
        layout = QVBoxLayout(self)

        self.web = QWebEngineView()
        self.web.load(QUrl("http://127.0.0.1:1234"))
        layout.addWidget(self.web, 2)

        self.project = project

    def start(self):
        data = self.project.compile()
        server.start_server(port=1234, data=data)
        self.resize(1000, 700)
        self.show()
        app.exec()
        server.stop_server()