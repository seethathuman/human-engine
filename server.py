#!/usr/bin/env python3
# Start/stop a simple development server

from flask import Flask
from multiprocessing import Process

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
    server_process.start()

def stop_server():
    global server_process
    server_process.terminate()
    server_process.join()

server_process = Process(target=run)
DATA = ""
PORT = 5000
if __name__ == "__main__":
    start_server()
    stop_server()