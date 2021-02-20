import os
import subprocess
from flask import Flask, request
app = Flask(__name__)

SIGNAL_USER = os.environ.get("SIGNAL_USER", None)
if not SIGNAL_USER:
    raise Exception("need to specify SIGNAL_USER")
SIGNAL_GROUP = os.environ.get("SIGNAL_GROUP", None)
if not SIGNAL_GROUP:
    raise Exception("need to specify SIGNAL_GROUP")
AUTH_SECRET = os.environ.get("AUTH_SECRET", None)
if not AUTH_SECRET:
    raise Exception("need to specify AUTH_SECRET")

@app.route("/webhook/<secret>", methods=["POST"])
def webhook(secret):
    if secret != AUTH_SECRET:
        return "wrong auth secret"
    obj = request.get_json()
    print(obj)
    message = f"""{obj.get("title")}
Message: {obj.get("message")}

Metrics:"""
    for m in obj["evalMatches"]:
        message += f"\n{m.get('metric')}: {m.get('value')}"

    subprocess.run(["signal-cli", "-u", SIGNAL_USER, "send", "-g", SIGNAL_GROUP], input=message.encode())

    return message
