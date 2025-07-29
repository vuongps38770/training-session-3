from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
import time
import signal
import sys

app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading')

def tail_log():
    with open("log.txt", "r") as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if line:
                socketio.emit("log", {"data": line})
            time.sleep(0.5)

@app.route("/")
def index():
    return render_template("index.html")

def signal_handler(sig, frame):
    print("\n[INFO] Đang thoát server...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    threading.Thread(target=tail_log, daemon=True).start()  # ← FIX: daemon=True
    socketio.run(app, host="0.0.0.0", port=5000)
