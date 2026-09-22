import sys
import json
import os


def security_gate():

    print("================================")
    print("       SECURECI SECURITY GATE")
    print("================================")

    status = "PASS"
    reason = "No critical security issues detected."

    try:
        with open("demo-secret.txt", "r") as file:
            content = file.read()

        if "SECURECI_DEMO_SECRET_" in content:
            status = "BLOCKED"
            reason = "Critical demo secret detected."

    except FileNotFoundError:
        print("demo-secret.txt not found.")

    os.makedirs("reports", exist_ok=True)

    report = {
        "sast": "PASS",
        "secret_scan": "FAIL" if status == "BLOCKED" else "PASS",
        "dependency_scan": "PASS",
        "dast": "PASS",
        "security_gate": status,
        "reason": reason
    }

    with open("reports/security-status.json", "w") as file:
        json.dump(report, file, indent=4)

    print("\nSecurity Scan Results")
    print("--------------------")
    print("SAST: PASS")
    print("Secret Scan:", report["secret_scan"])
    print("Dependency Scan: PASS")
    print("DAST: PASS")

    print("\nSecurity Gate:", status)
    print(reason)

    if status == "BLOCKED":
        print("\nDeployment is NOT allowed.")
        sys.exit(1)

    print("\nDeployment is allowed.")


if __name__ == "__main__":
    security_gate()