#!/usr/bin/env python3

from project import Project
import os.path
import server
import sys
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt, QUrl
from PySide6.QtWidgets import *
from PySide6.QtWebEngineWidgets import QWebEngineView

app = QApplication(sys.argv)

class Editor(QMainWindow):
    def __init__(self, project: Project):
        super().__init__()
        self.setWindowTitle("Human Engine Project Editor")
        self.setWindowIcon(QIcon("icon.png"))

        self.project = project
        self.unsaved = True

        self.file_tabs = FileTabs()
        self.project_browser = ProjectBrowser(project, self.file_tabs)
        self.web = QWebEngineView()
        self.web.load(QUrl("http://127.0.0.1:1234"))

        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        button_action = QAction("foo", self)
        button_action.setStatusTip("lorem ipsum dolor sit amet")
        button_action.triggered.connect(QApplication.quit)
        self.toolbar.addAction(button_action)

        self.project_browser_dock = QDockWidget("Project Browser",)
        self.project_browser_dock.setWidget(self.project_browser)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.project_browser_dock)

        self.web_dock = QDockWidget("Web Preview")
        self.web_dock.setWidget(self.web)
        self.splitDockWidget(self.project_browser_dock, self.web_dock, Qt.Orientation.Horizontal)

        self.file_tabs_dock = QDockWidget("Editor")
        self.file_tabs_dock.setWidget(self.file_tabs)
        self.splitDockWidget(self.web_dock, self.file_tabs_dock, Qt.Orientation.Horizontal)

        self.setStatusBar(QStatusBar(self))

    def stop(self):
        if self.unsaved:
            reply = QMessageBox.question(
                self, "Exit", "Do you want to save your unsaved changes before exiting?",
                QMessageBox.StandardButton.Save,
            )

    def start(self):
        data = self.project.compile()
        server.start_server(port=1234, data=data)
        self.resize(1000, 700)
        self.show()
        app.exec()
        server.stop_server()
        print("clean exit")

class FileTabs(QTabWidget):
    def __init__(self):
        super().__init__()

        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)
        self.open_files = {}

    def open(self, path):
        if path in self.open_files:
            self.setCurrentWidget(self.open_files[path])
            return

        editor = QTextEdit()

        with open(path, "r", encoding="utf8") as f:
            editor.setText(f.read())

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


class ProjectBrowser(QTreeWidget):
    def __init__(self, project, file_tabs):
        super().__init__()

        self.project = project
        self.open_file_callback = file_tabs.open

        self.setHeaderHidden(True)

        self.itemDoubleClicked.connect(self.open_item)

        self.populate()

    def populate(self):
        self.clear()

        scenes_root = QTreeWidgetItem(["Scenes"])
        resources_root = QTreeWidgetItem(["Resources"])
        other_root = QTreeWidgetItem(["Project Directory"])

        self.addTopLevelItem(scenes_root)
        self.addTopLevelItem(resources_root)
        self.addTopLevelItem(other_root)

        scenes = [entry["path"] for entry in self.project.config["scenes"].values()]
        resources = [entry["path"] for entry in self.project.config["resources"].values()]

        for path in scenes:
            item = QTreeWidgetItem([os.path.basename(path)])
            item.setData(0, Qt.ItemDataRole.UserRole, path)
            scenes_root.addChild(item)

        for path in resources:
            item = QTreeWidgetItem([os.path.basename(path)])
            item.setData(0, Qt.ItemDataRole.UserRole, path)
            resources_root.addChild(item)

        for root, _, files in os.walk(self.project.project_path):
            for f in files:
                full = os.path.join(root, f)

                if full in scenes or full in resources:
                    continue

                item = QTreeWidgetItem([f])
                item.setData(0, Qt.ItemDataRole.UserRole, full)
                other_root.addChild(item)

        self.expandAll()

    def open_item(self, item):
        path = item.data(0, Qt.ItemDataRole.UserRole)
        if path:
            self.open_file_callback(path)