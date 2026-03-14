#!/usr/bin/env python3

from editor.Editor import Editor
import project
project = project.Project(project_path=".test_project")
project.save()

editor = Editor(project=project)
editor.start()