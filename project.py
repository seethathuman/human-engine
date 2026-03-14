#!/usr/bin/env python3
# Human-Engine project
import json
from copy import deepcopy
from bs4 import BeautifulSoup
from json import dump
import os
import base64

default_config = {
    "title": "New Project",
    "scenes": {
        "default.xml": {
            "path": "default.xml"
        }
    },
    "resources": {
        "icon.png": {
            "path": "icon.png",
            "type":"image/png"
        }
    }
}

default_scene = """
<scene>
    <div class="title">
        <h1>Hello world! </h1>
        <img src="{data:#;base64,icon.png}" alt="My Image"/>
    </div>
    <ul style="font-size: 20px">
        <li> lorem ipsum dolor sit amet</li>
        <li> the quick brown fox jumps over a lazy dog </li>
        <li> test test 123 </li>
        <li> qwertyuiop1234567890!@#$%^&*()_+</li>
        <li> typewriter</li>
    </ul>
</scene>
"""

class Project:
    """Human Engine Project"""
    def __init__(self, project_path: str = "new_project"):
        self.scenes = {"default.xml": BeautifulSoup(default_scene, "xml")}
        self.config = default_config
        self.project_path = project_path

    def get_path(self, path: str):
        return os.path.normpath(os.path.join(self.project_path, path))

    def compile_scene(self, scene: BeautifulSoup):
        # replace all assets with base64 representation
        scene = deepcopy(scene)
        scene.scene.name = "div"
        for tag in scene.find_all(src=True):
            src = tag["src"]
            if not (src.startswith("{data:#;base64,") and  src.endswith("}")):
                continue
            src = src.strip("{}")
            prefix, data = src.split(",", 1)
            resource = self.config["resources"][data]
            with open(self.get_path(resource["path"]), "rb") as f:
                data = base64.b64encode(f.read()).decode("utf-8")
            prefix = prefix.replace("#", resource["type"], 1)
            tag["src"] = f"{prefix},{data}"
        return scene

    def compile(self):
        data = BeautifulSoup()
        # compile to standalone html file
        for name, scene in self.config["scenes"].items():
            with open(self.get_path(scene["path"])) as f:
                compiled_scene = self.compile_scene(BeautifulSoup(f.read(), "xml"))
            tag = data.new_tag("div", id=f"scene_{name}")
            tag.append(compiled_scene)
            data.body.append(tag)
        return data.prettify()

    def save(self):
        for name, data in self.scenes.items():
            scene = self.config["scenes"][name]
            with open(self.get_path(scene["path"]), "w") as f:
                f.write(data.prettify())

        with open(self.get_path("project.json"), "w") as f:
            json.dump(self.config, f, indent=4)








