import sys


def security_gate():
    print("================================")
    print("       SECURECI SECURITY GATE")
    print("================================")

    security_status = "PASS"

    print("\nChecking security policy...")

    # Demo security policy
    # SecureCI blocks deployment when a critical security
    # condition is detected.

    try:
        with open("demo-secret.txt", "r") as file:
            content = file.read()

        if "SECURECI_DEMO_SECRET_" in content:
            print("\n[CRITICAL] Demo secret detected!")
            security_status = "BLOCK"

    except FileNotFoundError:
        print("\nDemo secret test file not found.")

    print("\n--------------------------------")

    if security_status == "BLOCK":
        print("SECURITY GATE: BLOCK")
        print("Deployment is NOT allowed.")
        print("--------------------------------")
        sys.exit(1)

    print("SECURITY GATE: PASS")
    print("Deployment is allowed.")
    print("--------------------------------")


if __name__ == "__main__":
    security_gate()