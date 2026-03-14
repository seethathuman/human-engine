# Human Engine

## Introduction

An easier way to make self-contained web games.

Generate a single self-contained HTML file with all assets required
to run a webpage.

### Features
 - lightweight
 - resource system
 - scene system
 - editor to easily edit scenes
 - easy-to-use code editor.

## Usage

### Requirements
 - beautifulsoup4 (parse html)
 - lxml (xml parser used by bs4)
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