import json
import os
import shutil
import subprocess
import tempfile
from urllib.parse import urlparse

from git import Repo


REPORT_DIRECTORY = "reports"
FINAL_REPORT = os.path.join(
    REPORT_DIRECTORY,
    "vulnerability-report.json"
)


def validate_github_url(repo_url):
    parsed = urlparse(repo_url)

    return (
        parsed.scheme in ["http", "https"]
        and parsed.netloc.lower() == "github.com"
        and parsed.path.strip("/") != ""
    )


def clone_repository(repo_url):

    if not validate_github_url(repo_url):
        raise ValueError(
            "Please enter a valid public GitHub repository URL."
        )

    scan_directory = tempfile.mkdtemp(
        prefix="secureci_"
    )

    print("\n======================================")
    print("       SECURECI GITHUB SCANNER")
    print("======================================")

    print("\nRepository:")
    print(repo_url)

    print("\nCloning repository...")

    try:

        Repo.clone_from(
            repo_url,
            scan_directory
        )

        print("Repository cloned successfully.")

        return scan_directory

    except Exception as error:

        shutil.rmtree(
            scan_directory,
            ignore_errors=True
        )

        raise RuntimeError(
            f"Unable to clone repository: {error}"
        )


def run_command(command, working_directory):

    print("\nRunning:")
    print(" ".join(command))

    try:

        result = subprocess.run(
            command,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=300
        )

        return {
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except subprocess.TimeoutExpired:

        return {
            "return_code": -1,
            "stdout": "",
            "stderr": "Scanner timed out."
        }

    except FileNotFoundError:

        return {
            "return_code": -1,
            "stdout": "",
            "stderr": "Scanner is not installed or not available in PATH."
        }


def get_severity(value):

    if not value:
        return "MEDIUM"

    value = str(value).upper()

    if value in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        return value

    if value == "ERROR":
        return "HIGH"

    if value == "WARNING":
        return "MEDIUM"

    return "MEDIUM"


def parse_semgrep_report(report_file):

    findings = []

    if not os.path.exists(report_file):
        return findings

    try:

        with open(
            report_file,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

    except Exception:

        return findings

    for result in data.get("results", []):

        check_id = result.get(
            "check_id",
            "Unknown Semgrep Rule"
        )

        path = result.get(
            "path",
            "Unknown file"
        )

        start = result.get(
            "start",
            {}
        )

        line = start.get(
            "line",
            0
        )

        extra = result.get(
            "extra",
            {}
        )

        message = extra.get(
            "message",
            "Security issue detected by Semgrep."
        )

        severity = get_severity(
            extra.get("severity")
        )

        findings.append({

            "scanner": "Semgrep",

            "type": "Source Code Vulnerability",

            "rule": check_id,

            "severity": severity,

            "file": path,

            "line": line,

            "message": message,

            "status": "OPEN",

            "recommended_fix":
                "Review the affected code and "
                "apply the remediation recommended "
                "by SecureCI."
        })

    return findings


def parse_gitleaks_report(report_file):

    findings = []

    if not os.path.exists(report_file):
        return findings

    try:

        with open(
            report_file,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

    except Exception:

        return findings

    if not isinstance(data, list):
        return findings

    for leak in data:

        rule_id = leak.get(
            "RuleID",
            "Secret Detection"
        )

        description = leak.get(
            "Description",
            "Potential secret detected."
        )

        file_path = leak.get(
            "File",
            "Unknown file"
        )

        line = leak.get(
            "StartLine",
            0
        )

        findings.append({

            "scanner": "Gitleaks",

            "type": "Secret Exposure",

            "rule": rule_id,

            "severity": "HIGH",

            "file": file_path,

            "line": line,

            "message":
                "Potential secret or credential "
                "was detected in the repository.",

            "status": "OPEN",

            "recommended_fix":
                "Remove the secret from the source "
                "code and rotate the exposed credential."
        })

    return findings


def generate_report(
    repository_url,
    semgrep_findings,
    gitleaks_findings
):

    all_findings = (
        semgrep_findings +
        gitleaks_findings
    )

    severity_counts = {

        "CRITICAL": 0,
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0
    }

    for finding in all_findings:

        severity = finding.get(
            "severity",
            "MEDIUM"
        )

        if severity in severity_counts:

            severity_counts[severity] += 1

    report = {

        "project": "SecureCI",

        "repository": repository_url,

        "scan_status": "COMPLETED",

        "total_vulnerabilities":
            len(all_findings),

        "severity_summary":
            severity_counts,

        "security_gate":
            "BLOCKED"
            if len(all_findings) > 0
            else "PASS",

        "findings":
            all_findings
    }

    os.makedirs(
        REPORT_DIRECTORY,
        exist_ok=True
    )

    with open(
        FINAL_REPORT,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=4
        )

    return report


def scan_repository(repo_url):

    repository_directory = None

    try:

        repository_directory = clone_repository(
            repo_url
        )

        semgrep_report = os.path.join(
            repository_directory,
            "semgrep-report.json"
        )

        gitleaks_report = os.path.join(
            repository_directory,
            "gitleaks-report.json"
        )

        print("\n======================================")
        print("        RUNNING SECURITY SCANS")
        print("======================================")

        # -----------------------------
        # SEMGREP
        # -----------------------------

        semgrep_result = run_command(

            [
                "semgrep",
                "--config",
                "auto",
                "--json",
                "--output",
                "semgrep-report.json"
            ],

            repository_directory
        )

        # -----------------------------
        # GITLEAKS
        # -----------------------------

        gitleaks_result = run_command(

            [
                "gitleaks",
                "detect",
                "--source",
                ".",
                "--no-banner",
                "--report-format",
                "json",
                "--report-path",
                "gitleaks-report.json"
            ],

            repository_directory
        )

        # -----------------------------
        # PARSE RESULTS
        # -----------------------------

        semgrep_findings = parse_semgrep_report(
            semgrep_report
        )

        gitleaks_findings = parse_gitleaks_report(
            gitleaks_report
        )

        # -----------------------------
        # GENERATE UNIFIED REPORT
        # -----------------------------

        report = generate_report(

            repository_url,

            semgrep_findings,

            gitleaks_findings
        )

        # -----------------------------
        # DISPLAY SUMMARY
        # -----------------------------

        print("\n======================================")
        print("       SECURECI SCAN RESULTS")
        print("======================================")

        print(
            "\nTotal vulnerabilities:",
            report["total_vulnerabilities"]
        )

        print(
            "\nCRITICAL:",
            report["severity_summary"]["CRITICAL"]
        )

        print(
            "HIGH:",
            report["severity_summary"]["HIGH"]
        )

        print(
            "MEDIUM:",
            report["severity_summary"]["MEDIUM"]
        )

        print(
            "LOW:",
            report["severity_summary"]["LOW"]
        )

        print(
            "\nSecurity Gate:",
            report["security_gate"]
        )

        print(
            "\nReport generated:"
        )

        print(
            FINAL_REPORT
        )

        # -----------------------------
        # SHOW FINDINGS
        # -----------------------------

        print("\n======================================")
        print("          VULNERABILITIES")
        print("======================================")

        for index, finding in enumerate(
            report["findings"],
            start=1
        ):

            print(
                f"\n{index}. "
                f"{finding['scanner']} - "
                f"{finding['severity']}"
            )

            print(
                "   Type:",
                finding["type"]
            )

            print(
                "   File:",
                finding["file"]
            )

            print(
                "   Line:",
                finding["line"]
            )

            print(
                "   Message:",
                finding["message"]
            )

            print(
                "   Recommended Fix:",
                finding["recommended_fix"]
            )

        return report

    finally:

        if repository_directory:

            shutil.rmtree(
                repository_directory,
                ignore_errors=True
            )


if __name__ == "__main__":

    repository_url = input(
        "\nEnter public GitHub repository URL: "
    ).strip()

    try:

        scan_repository(
            repository_url
        )

    except Exception as error:

        print("\n======================================")
        print("          SECURECI ERROR")
        print("======================================")

        print(error)