#!/usr/bin/env python3
# Start/stop a simple development server

from flask import Flask
from multiprocessing import Process
from time import sleep
app = Flask(__name__)

@app.route("/")
def index():
    global DATA
    return DATA

@app.errorhandler(404)
def error404(path: str):
    global DATA
    return DATA

def run():
    global app
    global PORT
    app.run(port=PORT, use_reloader=False)

def start_server(data: str = "<p>hello world!<p>", port: int = 5000):
    global server_process
    global DATA
    global PORT
    PORT = port
    DATA = data
    if server_process:
        stop_server()
    server_process = Process(target=run)
    server_process.start()
    sleep(0.25)

def stop_server():
    global server_process
    if server_process:
        server_process.terminate()
        server_process.join()
    server_process = None

server_process: Process | None = None
DATA: str = ""
PORT: int = 5000
if __name__ == "__main__":
    start_server()
    stop_server()