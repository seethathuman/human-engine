#!/usr/bin/env python3
# Human-Engine project
from copy import deepcopy

from bs4 import BeautifulSoup
import os
import base64

default_config = """
<config>
    <title>New Project</title>
    <scenes>
        <scene>
            <path>default.xml</path>
        </scene>
    </scenes>
    <resources>
        <resource>
            <path>icon.png</path>
            <type>image/png</type>
        </resource>
    </resources>
</config>
"""

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
        self.config = BeautifulSoup(default_config, "xml")
        self.project_path = project_path

    def get_resource(self, path: str):
        resources = self.config.resources.find_all("resource")
        for resource in resources:
            if resource.path.text == path:
                return resource
        raise FileNotFoundError

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
            resource = self.get_resource(data)
            with open(self.get_path(resource.path.text), "rb") as f:
                data = base64.b64encode(f.read()).decode("utf-8")
            prefix = prefix.replace("#", resource.type.text, 1)
            tag["src"] = f"{prefix},{data}"
        return scene

    def compile(self):
        data = ""
        # compile to standalone html file
        for scene in self.config.scenes.find_all(recursive=False):
            with open(self.get_path(scene.path.text)) as f:
                compiled_scene = self.compile_scene(BeautifulSoup(f.read(), "xml"))
            # later: implement scene switching
            data += compiled_scene.prettify()
        return data

    def save(self):
        self.config.config.scenes.clear()
        for name, scene in self.scenes.items():
            scene_tag = self.config.new_tag("scene")
            path_tag = self.config.new_tag("path")
            path_tag.string = name
            scene_tag.append(path_tag)
            self.config.config.scenes.append(scene_tag)

            with open(self.get_path(name), "w") as f:
                f.write(scene.prettify())

        with open(self.get_path("project.xml"), "w") as f:
            f.write(self.config.prettify())








