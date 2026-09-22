from flask import Flask, render_template

app = Flask(__name__)

# Demo secret for SecureCI testing
DEMO_AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"


@app.route("/")
def home():
    return render_template("index.html")


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