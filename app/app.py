from flask import Flask, render_template
import os
import json

app = Flask(__name__)


@app.route("/")
def home():

    security_status = {
        "sast": "PASS",
        "secret_scan": "FAIL",
        "dependency_scan": "PASS",
        "dast": "PASS",
        "security_gate": "BLOCKED"
    }

    return render_template(
        "index.html",
        status=security_status
    )


@app.route("/login")
def login():
    return """
    <h2>Student Store Login</h2>

    <form>
        <input type="text" placeholder="Username">
        <br><br>

        <input type="password" placeholder="Password">
        <br><br>

        <button type="submit">Login</button>
    </form>
    """


@app.route("/dashboard")
def dashboard():
    return """
    <h2>Student Store Dashboard</h2>
    <p>Welcome to the Student Store.</p>
    <p>This application is being tested by SecureCI.</p>
    """


if __name__ == "__main__":
    app.run(debug=True)