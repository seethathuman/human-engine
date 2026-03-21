#!/usr/bin/env python

from PySide6.QtCore import Qt
from PySide6.QtWidgets import *

class SceneTree(QTreeWidget):
    def __init__(self):
        super().__init__()

        self.scene = {}
        self.open_callback = None
        self.objects = []
        self.setIndentation(12)
        self.setHeaderHidden(True)
        self.setExpandsOnDoubleClick(True)
        self.itemClicked.connect(self.open_item)

    def set_scene(self, scene):
        self.scene = scene

    def set_editor(self, editor):
        self.open_callback = editor.open

    def populate(self):
        self.clear()
        self.objects = []
        root = QTreeWidgetItem([self.scene["name"]])
        root.setData(0, Qt.ItemDataRole.UserRole, 0)
        self.objects.append(self.scene)
        self.addTopLevelItem(root)
        self.populate_children(self.scene["content"], root)
        self.expandAll()

    def populate_children(self, content, parent):
        for child in content:
            item = QTreeWidgetItem([child["name"]])
            item.setData(0, Qt.ItemDataRole.UserRole, len(self.objects))
            self.objects.append(child)
            parent.addChild(item)
            if isinstance(child["content"], list):
                self.populate_children(child["content"], item)

    def open_item(self, item):
        data = item.data(0, Qt.ItemDataRole.UserRole)
        self.open_callback(self.objects[data])
