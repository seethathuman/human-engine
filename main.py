#!/usr/bin/env python3

import editor
import project
project = project.Project(project_path="test_project")
project.save()

editor = editor.Editor(project=project)
editor.start()