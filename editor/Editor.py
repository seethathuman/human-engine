#!/usr/bin/env python3

from project import Project
from editor.FileTabs import FileTabs
from editor.ProjectBrowser import ProjectBrowser
import server
import sys
import traceback
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt, QUrl, QSize
from PySide6.QtWidgets import *
from PySide6.QtWebEngineWidgets import QWebEngineView

app = QApplication(sys.argv)

class Editor(QMainWindow):
    def __init__(self, project: Project):
        super().__init__()
        self.setWindowTitle("Human Engine Project Editor")
        self.setWindowIcon(QIcon("resources/icon.png"))

        self.project = project
        self.toolbar_visible = True

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

        # Initialize Docks
        self.file_tabs = FileTabs()
        self.project_browser = ProjectBrowser(project, self.file_tabs)

        web_container = QWidget()
        web_layout = QVBoxLayout(web_container)
        self.web = QWebEngineView()
        self.web.load(QUrl("http://127.0.0.1:5337"))
        self.web_toolbar = QToolBar()
        self.web_toolbar.setIconSize(QSize(16, 16))
        refresh_action = QAction("Reload", self)
        refresh_action.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.ViewRefresh))
        refresh_action.setStatusTip("Reload the preview.")
        refresh_action.triggered.connect(self._refresh_browser)
        self.web_toolbar.addAction(refresh_action)
        self.view_menu.addAction(refresh_action)
        web_layout.addWidget(self.web_toolbar)
        web_layout.addWidget(self.web)

        self.project_browser_dock = QDockWidget("Project Browser",)
        self.project_browser_dock.setWidget(self.project_browser)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.project_browser_dock)

        self.web_dock = QDockWidget("Web Preview")
        self.web_dock.setWidget(web_container)
        self.splitDockWidget(self.project_browser_dock, self.web_dock, Qt.Orientation.Horizontal)

        self.file_tabs_dock = QDockWidget("Editor")
        self.file_tabs_dock.setWidget(self.file_tabs)
        self.splitDockWidget(self.web_dock, self.file_tabs_dock, Qt.Orientation.Horizontal)

    def _refresh_browser(self):
        self.web.hide()
        data = self.project.compile()
        with open(self.project.get_path("_.html"), "w") as f:
            f.write(data)
        server.stop_server()
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
        # TODO: implement project saving and loading
        pass

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