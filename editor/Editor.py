#!/usr/bin/env python3
import json

from editor.PropertyEditor import PropertyEditor
from project import Project
from editor.FileTabs import FileTabs
from editor.ProjectBrowser import ProjectBrowser
from editor.SceneTree import SceneTree
from editor.WebView import WebView
import server
import sys
import traceback
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import *

app = QApplication(sys.argv)

class Editor(QMainWindow):
    def __init__(self, project: Project):
        super().__init__()
        self.setWindowTitle("Human Engine Project Editor")
        self.setWindowIcon(QIcon("resources/icon.png"))

        self.project = project
        self.toolbar_visible = True
        self.scene_name = next(iter(self.project.config["scenes"].keys()))

        # Initialize Menu and Toolbar
        self.setStatusBar(QStatusBar(self))
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)
        self.menubar = self.menuBar()
        self.file_menu = self.menubar.addMenu("&File")
        self.view_menu = self.menubar.addMenu("&View")

        self.toggle_toolbar_action = QAction("Toggle &Toolbar", self)
        self.toggle_toolbar_action.setIcon(QIcon.fromTheme("checkbox"))
        self.toggle_toolbar_action.setStatusTip("Toggle the toolbar.")
        self.toggle_toolbar_action.triggered.connect(self._toggle_toolbar)
        self.view_menu.addAction(self.toggle_toolbar_action)

        exit_action = QAction("E&xit", self)
        exit_action.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.ApplicationExit))
        exit_action.setStatusTip("Exit the editor.")
        exit_action.triggered.connect(self._stop)
        self.toolbar.addAction(exit_action)
        self.file_menu.addAction(exit_action)

        save_action = QAction("&Save", self)
        save_action.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSave))
        save_action.setStatusTip("Save the current scene.")
        save_action.triggered.connect(self._save_project)
        self.toolbar.addAction(save_action)
        self.file_menu.addAction(save_action)

        self.web_toolbar = QToolBar()
        self.web_toolbar.setIconSize(QSize(16, 16))
        refresh_action = QAction("Reload", self)
        refresh_action.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.ViewRefresh))
        refresh_action.setStatusTip("Reload the preview.")
        refresh_action.triggered.connect(self._refresh_browser)
        self.web_toolbar.addAction(refresh_action)
        self.view_menu.addAction(refresh_action)

        # Initialize Docks
        self.file_tabs = FileTabs()
        self.project_browser = ProjectBrowser()
        self.scene_tree = SceneTree()
        self.web = WebView()

        self.property_editor = PropertyEditor()
        self.project_browser.set_project(project)
        self.project_browser.set_editor(self.file_tabs)
        self.project_browser.populate()
        with open(self.project.get_path(self.scene_name)) as f:
            self.scene_data = json.load(f)
        self.scene_tree.set_scene(self.scene_data)
        self.scene_tree.set_editor(self.property_editor)
        self.scene_tree.populate()
        self.web.set_toolbar(self.web_toolbar)

        self.web_dock = QDockWidget("Web Preview")
        self.web_dock.setWidget(self.web)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.web_dock)

        self.property_editor_dock = QDockWidget("Properties")
        self.property_editor_dock.setWidget(self.property_editor)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.property_editor_dock)
        self.splitDockWidget(self.web_dock, self.property_editor_dock, Qt.Orientation.Horizontal)

        self.file_tabs_dock = QDockWidget("Editor")
        self.file_tabs_dock.setWidget(self.file_tabs)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.file_tabs_dock)
        self.tabifyDockWidget(self.web_dock, self.file_tabs_dock)
        self.web_dock.raise_()

        self.scene_tree_dock = QDockWidget("Scene Tree")
        self.scene_tree_dock.setWidget(self.scene_tree)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.scene_tree_dock)

        self.project_browser_dock = QDockWidget("Project Browser")
        self.project_browser_dock.setWidget(self.project_browser)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.project_browser_dock)

    def _refresh_browser(self):
        self.web.hide()
        self._save_project()
        server.stop_server()
        with open(self.project.get_path("_.html")) as f: data = f.read()
        server.start_server(port=5337, data=data)
        self.web.reload()
        self.web.show()

    def _toggle_toolbar(self):
        if self.toolbar_visible:
            self.toolbar.hide()
            self.toggle_toolbar_action.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.ProcessStop))
        else:
            self.toolbar.show()
            self.toggle_toolbar_action.setIcon(QIcon.fromTheme("checkbox"))
        self.toolbar_visible ^= 1

    def _stop(self):
        reply = QMessageBox.question(
            self, "Exit", "Are you sure you want to exit and discard unsaved changes?",
            QMessageBox.StandardButton.Discard |
            QMessageBox.StandardButton.Cancel
        )
        if reply == QMessageBox.StandardButton.Cancel: return
        QApplication.quit()

    def _save_project(self):
        with open(self.project.get_path(self.scene_name), "w") as f:
            json.dump(self.scene_data, f, indent=4)
            print(f"SCENE: {self.scene_data}")
        data = self.project.compile()
        with open(self.project.get_path("_.html"), "w") as f:
            f.write(data)

    def start(self):
        data = self.project.compile()
        with open(self.project.get_path("_.html"), "w") as f:
            f.write(data)
        server.start_server(port=5337, data=data)
        self.show()
        app.exec()
        server.stop_server()
        print("clean exit")

def exception_hook(exc_type: type[BaseException], exc_value: BaseException, exc_traceback):
    print("Exception caught!")
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    traceback.print_exception(exc_type, exc_value, exc_traceback)
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(f"{exc_type.__name__}")
    msg.setText(f"An uncaught {exc_type.__name__} has occurred.")
    msg.setDetailedText(error_msg)
    msg.setStandardButtons(QMessageBox.StandardButton.Close | QMessageBox.StandardButton.Ignore)
    msg.setDefaultButton(QMessageBox.StandardButton.Close)
    result = msg.exec()
    if result == QMessageBox.StandardButton.Ignore:
        return
    QApplication.quit()

sys.excepthook = exception_hook