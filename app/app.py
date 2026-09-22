from flask import Flask, render_template
import os
import json

app = Flask(__name__)


@app.route("/")
@app.route("/")
def home():

    default_status = {
        "sast": "NOT SCANNED",
        "secret_scan": "NOT SCANNED",
        "dependency_scan": "NOT SCANNED",
        "dast": "NOT SCANNED",
        "security_gate": "NOT SCANNED",
        "reason": "No scan report available."
    }

    try:
        with open("reports/security-status.json", "r") as file:
            security_status = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        security_status = default_status

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