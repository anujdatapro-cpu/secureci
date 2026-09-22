import os
import subprocess
import sys
import time
import webbrowser


PROJECT_DIRECTORY = os.path.dirname(
    os.path.abspath(__file__)
)

DASHBOARD_URL = "http://127.0.0.1:5000"


def print_banner():

    print()
    print("==============================================")
    print("              SECURECI")
    print("       DevSecOps Security Scanner")
    print("==============================================")
    print()


def check_git_repository():

    git_directory = os.path.join(
        PROJECT_DIRECTORY,
        ".git"
    )

    return os.path.exists(git_directory)


def get_git_remote():

    try:

        result = subprocess.run(
            [
                "git",
                "config",
                "--get",
                "remote.origin.url"
            ],
            cwd=PROJECT_DIRECTORY,
            capture_output=True,
            text=True
        )

        remote_url = result.stdout.strip()

        if not remote_url:
            return None

        # Convert GitHub SSH URL to HTTPS
        if remote_url.startswith("git@github.com:"):

            remote_url = remote_url.replace(
                "git@github.com:",
                "https://github.com/"
            )

        # Remove .git from the end
        if remote_url.endswith(".git"):

            remote_url = remote_url[:-4]

        return remote_url

    except Exception:

        return None


def run_security_scan(repository_url):

    print()
    print("----------------------------------------------")
    print("STEP 1 — SECURITY SCAN")
    print("----------------------------------------------")

    print()
    print("Repository detected:")
    print(repository_url)

    print()
    print("Starting security scanners...")
    print()

    scanner_file = os.path.join(
        PROJECT_DIRECTORY,
        "github_scanner.py"
    )

    if not os.path.exists(scanner_file):

        print()
        print("ERROR:")
        print("github_scanner.py was not found.")

        return 1

    try:

        # The current github_scanner.py asks for
        # the repository URL using input().
        #
        # We automatically provide the detected
        # repository URL to it.

        result = subprocess.run(
            [
                sys.executable,
                scanner_file
            ],
            cwd=PROJECT_DIRECTORY,
            input=repository_url + "\n",
            text=True
        )

        print()

        print("----------------------------------------------")

        if result.returncode == 0:

            print("SecureCI scan completed successfully.")

        else:

            print(
                "SecureCI scan finished with "
                "an error."
            )

        print("----------------------------------------------")

        return result.returncode

    except Exception as error:

        print()
        print("ERROR while running security scanner:")
        print(error)

        return 1


def start_dashboard():

    print()
    print("----------------------------------------------")
    print("STEP 2 — SECURECI DASHBOARD")
    print("----------------------------------------------")

    dashboard_file = os.path.join(
        PROJECT_DIRECTORY,
        "app",
        "app.py"
    )

    if not os.path.exists(dashboard_file):

        print()
        print("ERROR:")
        print("app/app.py was not found.")

        return None

    print()
    print("Starting SecureCI web dashboard...")

    try:

        dashboard_process = subprocess.Popen(
            [
                sys.executable,
                dashboard_file
            ],
            cwd=PROJECT_DIRECTORY
        )

        # Give Flask time to start
        time.sleep(3)

        print()
        print("Dashboard started successfully.")

        print()
        print("Opening:")
        print(DASHBOARD_URL)

        webbrowser.open(
            DASHBOARD_URL
        )

        return dashboard_process

    except Exception as error:

        print()
        print("ERROR starting dashboard:")
        print(error)

        return None


def main():

    print_banner()

    print("SecureCI project:")
    print(PROJECT_DIRECTORY)

    print()

    # ==========================================
    # STEP 0
    # ==========================================

    print("----------------------------------------------")
    print("STEP 0 — REPOSITORY CHECK")
    print("----------------------------------------------")

    if not check_git_repository():

        print()
        print(
            "ERROR: This folder is not a Git repository."
        )

        print()
        print(
            "Run SecureCI from a Git project folder."
        )

        print()
        print("Example:")
        print(
            "cd D:\\Projects\\MyProject"
        )
        print(
            "python secureci.py"
        )

        sys.exit(1)

    print()
    print("Git repository detected.")

    # ==========================================
    # GET GITHUB REMOTE
    # ==========================================

    repository_url = get_git_remote()

    if not repository_url:

        print()
        print(
            "ERROR: No GitHub remote repository found."
        )

        print()
        print(
            "Make sure this project has a GitHub remote."
        )

        print()
        print("Example:")
        print(
            "git remote add origin "
            "https://github.com/user/project.git"
        )

        sys.exit(1)

    print()
    print("GitHub repository:")
    print(repository_url)

    # ==========================================
    # RUN SECURITY SCAN
    # ==========================================

    scan_result = run_security_scan(
        repository_url
    )

    # ==========================================
    # START DASHBOARD
    # ==========================================

    dashboard_process = start_dashboard()

    if dashboard_process is None:

        sys.exit(1)

    # ==========================================
    # FINAL STATUS
    # ==========================================

    print()
    print("==============================================")
    print("        SECURECI IS RUNNING")
    print("==============================================")

    print()
    print(
        "Security scan completed."
    )

    print()
    print(
        "Dashboard:"
    )

    print(
        DASHBOARD_URL
    )

    print()
    print(
        "Keep this terminal open while using SecureCI."
    )

    print()
    print(
        "Press CTRL+C to stop SecureCI."
    )

    try:

        dashboard_process.wait()

    except KeyboardInterrupt:

        print()
        print(
            "Stopping SecureCI..."
        )

        dashboard_process.terminate()

        print(
            "SecureCI stopped."
        )


if __name__ == "__main__":

    main()