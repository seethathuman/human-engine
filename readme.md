# Human Engine

## Introduction

Human Engine is a lightweight game engine based on Qt and Python3 
designed to be an easier way to make self-contained web games with
visual based code.

Generates a single self-contained HTML file with all assets required
to run a webpage.

### Features
 - resource system
 - scene system
 - editor to edit scenes
 - visual code editor.

## Usage

### Requirements
 - beautifulsoup4 (parse html)
 - lxml
 - PySide6 (qt gui editor)
 - flask (web preview)

### Install

1. Clone the repo
```bash
git clone https://github.com/seethathuman/human-engine.git
cd human-engine
```

2. Install the dependencies
```bash
python3 -m pip install -r requirements.txt
```

3. Run the editor
```bash
python3 ./main.py
```