#!/usr/bin/env python3

import json
from bs4 import BeautifulSoup, Tag
from resources.templates import DEFAULT_CONFIG, DEFAULT_SCENES
import base64
import os

class Project:
    """Human Engine Project"""
    def __init__(self, project_path: str = "new_project"):
        self.project_path = project_path
        self.config = {}
        if not os.path.exists(project_path):
            self.create_project(DEFAULT_CONFIG, DEFAULT_SCENES)
        self.load_project()

    def create_project(self, config: dict, scenes: dict) -> None:
        os.mkdir(self.project_path)
        with open(self.get_path("project.json"), "w") as f:
            json.dump(config, f, indent=4)

        for scene, data in scenes.items():
            with open(self.get_path(scene), "w") as f:
                json.dump(data, f, indent=4)

    def load_project(self) -> None:
        with open(self.get_path("project.json")) as f:
            self.config = json.load(f)

    def get_path(self, path: str) -> str:
        return os.path.normpath(os.path.join(self.project_path, path))

    def compile_content(self, content: list | str, tag: Tag, soup: BeautifulSoup) -> Tag:
        if isinstance(content, str): # no children
            tag.string = content
            return tag

        for element in content: # construct contents of a bs4 tag
            properties = element["properties"].copy() # save a local copy to modify
            if "src-path" in properties: # base64 encode resource
                resource = self.config["resources"][properties["src-path"]]
                with open(self.get_path(resource["path"]), "rb") as f:
                    data = f.read()
                properties["src"] = f"data:{resource["type"]};base64,{base64.b64encode(data).decode("utf-8")}"
                del properties["src-path"]
            if "style" in properties:
                properties["style"] = ";".join([f"{k}:{v}" for k, v in properties["style"].items()])

            child = soup.new_tag(element["type"], **properties)
            self.compile_content(element["content"], child, soup)
            tag.append(child)
        return tag

    def compile(self) -> str:
        soup = BeautifulSoup("<head/><body/>", "lxml")
        for name, scene in self.config["scenes"].items():
            with open(self.get_path(scene["path"])) as f:
                data = json.load(f)
            scene_tag = soup.new_tag("div")
            scene_tag["class"] = "scene-root"
            scene_tag["id"] = f"scene-{name}"
            self.compile_content(data["content"], scene_tag, soup)
            soup.body.append(scene_tag)
        return soup.prettify()

    def save(self):
        with open(self.get_path("project.json"), "w") as f:
            json.dump(self.config, f, indent=4)