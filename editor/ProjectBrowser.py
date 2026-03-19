#!/usr/bin/env python

import os.path
from PySide6.QtCore import Qt
from PySide6.QtWidgets import *

class ProjectBrowser(QTreeWidget):
    def __init__(self):
        super().__init__()

        self.project = None
        self.open_file_callback = None

        self.setIndentation(12)
        self.setHeaderHidden(True)
        self.itemDoubleClicked.connect(self.open_item)
        self.setExpandsOnDoubleClick(False)

    def set_project(self, project):
        self.project = project

    def set_editor(self, editor):
        self.open_file_callback = editor.open

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
            item = QTreeWidgetItem([path])
            item.setData(0, Qt.ItemDataRole.UserRole, self.project.get_path(path))
            scenes_root.addChild(item)

        for path in resources:
            item = QTreeWidgetItem([path])
            item.setData(0, Qt.ItemDataRole.UserRole, self.project.get_path(path))
            resources_root.addChild(item)

        excluded = ["_.html"]
        for root, _, files in os.walk(self.project.project_path):
            for f in files:
                full = os.path.join(root, f)

                if f in [*scenes, *resources, *excluded]:
                    continue

                item = QTreeWidgetItem([f])
                item.setData(0, Qt.ItemDataRole.UserRole, full)
                other_root.addChild(item)

        self.expandAll()

    def open_item(self, item):
        path = item.data(0, Qt.ItemDataRole.UserRole)
        if path:
            self.open_file_callback(path)