from flask import Flask, render_template, redirect, url_for
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime


app = Flask(__name__)


BASE_DIRECTORY = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


REPORT_FILE = os.path.join(
    BASE_DIRECTORY,
    "reports",
    "vulnerability-report.json"
)


PREVIOUS_REPORT_FILE = os.path.join(
    BASE_DIRECTORY,
    "reports",
    "previous-report.json"
)


SCANNER_FILE = os.path.join(
    BASE_DIRECTORY,
    "github_scanner.py"
)


def default_report():

    return {
        "project": "SecureCI",
        "repository": "No repository scanned",
        "scan_status": "NOT SCANNED",

        "total_vulnerabilities": 0,

        "severity_summary": {
            "CRITICAL": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0
        },

        "security_gate": "NOT SCANNED",

        "findings": [],

        "scan_time": "Not available"
    }


def load_report():

    if not os.path.exists(REPORT_FILE):
        return default_report()


    try:

        with open(
            REPORT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            report = json.load(file)


        report.setdefault(
            "project",
            "SecureCI"
        )

        report.setdefault(
            "repository",
            "Unknown"
        )

        report.setdefault(
            "scan_status",
            "COMPLETED"
        )

        report.setdefault(
            "severity_summary",
            {
                "CRITICAL": 0,
                "HIGH": 0,
                "MEDIUM": 0,
                "LOW": 0
            }
        )

        report.setdefault(
            "findings",
            []
        )

        report.setdefault(
            "security_gate",
            "PASS"
        )

        report.setdefault(
            "scan_time",
            "Not available"
        )


        report["total_vulnerabilities"] = len(
            report["findings"]
        )


        for finding in report["findings"]:

            finding.setdefault(
                "scanner",
                "Security Scanner"
            )

            finding.setdefault(
                "severity",
                "MEDIUM"
            )

            finding.setdefault(
                "type",
                "Security Vulnerability"
            )

            finding.setdefault(
                "rule",
                "Security Rule"
            )

            finding.setdefault(
                "file",
                "Unknown"
            )

            finding.setdefault(
                "line",
                "Unknown"
            )

            finding.setdefault(
                "message",
                "A security issue was detected."
            )

            finding.setdefault(
                "recommended_fix",
                "Review and fix the reported issue."
            )


        return report


    except Exception as error:

        print("Error reading report:")
        print(error)

        return default_report()


def save_previous_report():

    if os.path.exists(REPORT_FILE):

        try:

            shutil.copy2(
                REPORT_FILE,
                PREVIOUS_REPORT_FILE
            )

            print(
                "Previous security report saved."
            )

        except Exception as error:

            print(
                "Could not save previous report:"
            )

            print(error)


def run_rescan():

    report = load_report()

    repository = report.get(
        "repository",
        ""
    )


    if not repository:

        return False


    if not os.path.exists(SCANNER_FILE):

        print(
            "github_scanner.py was not found."
        )

        return False


    save_previous_report()


    print()
    print("=" * 55)
    print("SECURECI RESCAN STARTED")
    print("=" * 55)
    print()
    print(
        "Repository:",
        repository
    )


    try:

        result = subprocess.run(

            [
                sys.executable,
                SCANNER_FILE
            ],

            input=repository + "\n",

            text=True,

            capture_output=True,

            cwd=BASE_DIRECTORY
        )


        print()
        print("Scanner output:")
        print(result.stdout)


        if result.stderr:

            print()
            print("Scanner messages:")
            print(result.stderr)


        # Add latest scan time to the report

        if os.path.exists(REPORT_FILE):

            try:

                with open(
                    REPORT_FILE,
                    "r",
                    encoding="utf-8"
                ) as file:

                    new_report = json.load(file)


                new_report["scan_time"] = (
                    datetime.now().strftime(
                        "%d %b %Y, %I:%M %p"
                    )
                )


                with open(
                    REPORT_FILE,
                    "w",
                    encoding="utf-8"
                ) as file:

                    json.dump(
                        new_report,
                        file,
                        indent=4
                    )


            except Exception as error:

                print(
                    "Could not update scan time:"
                )

                print(error)


        return True


    except Exception as error:

        print()
        print("RESCAN ERROR")
        print(error)

        return False


@app.route("/")
def home():

    report = load_report()

    previous_report = None


    if os.path.exists(
        PREVIOUS_REPORT_FILE
    ):

        try:

            with open(
                PREVIOUS_REPORT_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                previous_report = json.load(file)

        except Exception:

            previous_report = None


    return render_template(
        "dashboard.html",
        report=report,
        previous_report=previous_report
    )


@app.route(
    "/rescan",
    methods=["POST"]
)
def rescan():

    run_rescan()

    return redirect(
        url_for("home")
    )


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )