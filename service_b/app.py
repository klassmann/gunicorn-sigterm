import random

from flask import Flask, g
import time

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return "OK", 200


@app.route("/hang_on", methods=["GET"])
def test():
    g.stop_exec = False
    count = random.randint(2, 30)
    while count > 0:
        count -= 1
        print(count)
        time.sleep(1)
    print("closing")
    return "OK", 200
