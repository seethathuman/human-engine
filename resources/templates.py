DEFAULT_SCENES = {
    "default.hsc":
        {
            "name": "default.hsc",
            "type": "div",
            "properties": {
                "class": "scene-root"
            },
            "content": [
                {
                    "name": "Header container",
                    "type": "div",
                    "properties": {
                        "class": "title"
                    },
                    "content": [
                        {
                            "name": "Title",
                            "type": "h1",
                            "properties": {},
                            "content": "hello world"
                        },
                        {
                            "name": "Header Image",
                            "type": "img",
                            "properties": {
                                "src-path": "icon.png",
                                "alt": "Header Image"
                            },
                            "content": ""
                        }
                    ]
                },
                {
                    "name": "Test Bullet List",
                    "type": "ul",
                    "properties": {
                        "style": {
                            "font-size": "200%"
                        }
                    },
                    "content": [
                        {
                            "name": "Test Point 1",
                            "type": "li",
                            "properties": {
                            },
                            "content": "lorem ipsum"
                        }
                    ]
                }
            ]
        }
}
DEFAULT_CONFIG = {
    "title": "New Project",
    "scenes": {
        "default.hsc": {
            "path": "default.hsc"
        }
    },
    "resources": {
        "icon.png": {
            "path": "icon.png",
            "type": "image/png"
        }
    }
}