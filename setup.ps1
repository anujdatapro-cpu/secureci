# ============================================================
# SECURECI SETUP SCRIPT
# ============================================================

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================================"
Write-Host "              SECURECI INSTALLATION SETUP"
Write-Host "============================================================"
Write-Host ""

# ============================================================
# CHECK PYTHON
# ============================================================

Write-Host "[1/6] Checking Python..."

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {

    Write-Host ""
    Write-Host "ERROR: Python was not found." -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python 3.10 or newer."
    Write-Host ""

    exit 1
}

$pythonVersion = python --version

Write-Host "Python found: $pythonVersion" -ForegroundColor Green


# ============================================================
# CHECK GIT
# ============================================================

Write-Host ""
Write-Host "[2/6] Checking Git..."

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {

    Write-Host ""
    Write-Host "ERROR: Git was not found." -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Git and run setup again."
    Write-Host ""

    exit 1
}

$gitVersion = git --version

Write-Host "Git found: $gitVersion" -ForegroundColor Green


# ============================================================
# CREATE VIRTUAL ENVIRONMENT
# ============================================================

Write-Host ""
Write-Host "[3/6] Preparing Python virtual environment..."

if (-not (Test-Path "venv")) {

    Write-Host "Creating virtual environment..."

    python -m venv venv

    if ($LASTEXITCODE -ne 0) {

        Write-Host ""
        Write-Host "ERROR: Could not create virtual environment." -ForegroundColor Red

        exit 1
    }

    Write-Host "Virtual environment created." -ForegroundColor Green

}
else {

    Write-Host "Virtual environment already exists." -ForegroundColor Green
}


# ============================================================
# FIND VIRTUAL ENVIRONMENT PYTHON
# ============================================================

$venvPython = Join-Path $PSScriptRoot "venv\Scripts\python.exe"

if (-not (Test-Path $venvPython)) {

    Write-Host ""
    Write-Host "ERROR: Virtual environment Python was not found." -ForegroundColor Red

    exit 1
}


# ============================================================
# INSTALL PYTHON DEPENDENCIES
# ============================================================

Write-Host ""
Write-Host "[4/6] Installing SecureCI Python dependencies..."

& $venvPython -m pip install --upgrade pip

if ($LASTEXITCODE -ne 0) {

    Write-Host ""
    Write-Host "ERROR: Could not upgrade pip." -ForegroundColor Red

    exit 1
}

& $venvPython -m pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {

    Write-Host ""
    Write-Host "ERROR: Could not install SecureCI dependencies." -ForegroundColor Red

    exit 1
}

Write-Host ""
Write-Host "Python dependencies installed successfully." -ForegroundColor Green


# ============================================================
# CHECK SEMGREP
# ============================================================

Write-Host ""
Write-Host "[5/6] Checking security scanners..."

$semgrepPath = Join-Path $PSScriptRoot "venv\Scripts\semgrep.exe"

if (Test-Path $semgrepPath) {

    $semgrepVersion = & $semgrepPath --version

    Write-Host "Semgrep: $semgrepVersion" -ForegroundColor Green

}
else {

    Write-Host "WARNING: Semgrep was not found." -ForegroundColor Yellow
}


# ============================================================
# CHECK PIP-AUDIT
# ============================================================

$pipAuditPath = Join-Path $PSScriptRoot "venv\Scripts\pip-audit.exe"

if (Test-Path $pipAuditPath) {

    $pipAuditVersion = & $pipAuditPath --version

    Write-Host "pip-audit: $pipAuditVersion" -ForegroundColor Green

}
else {

    Write-Host "WARNING: pip-audit was not found." -ForegroundColor Yellow
}


# ============================================================
# CHECK GITLEAKS
# ============================================================

Write-Host ""
Write-Host "[6/6] Checking Gitleaks..."

if (Get-Command gitleaks -ErrorAction SilentlyContinue) {

    $gitleaksVersion = gitleaks version

    Write-Host "Gitleaks: $gitleaksVersion" -ForegroundColor Green

}
else {

    Write-Host ""
    Write-Host "WARNING: Gitleaks was not found." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Install Gitleaks separately using:"
    Write-Host ""
    Write-Host "winget install --id Gitleaks.Gitleaks -e"
    Write-Host ""
}


# ============================================================
# FINAL MESSAGE
# ============================================================

Write-Host ""
Write-Host "============================================================"
Write-Host "             SECURECI SETUP COMPLETED"
Write-Host "============================================================"
Write-Host ""

Write-Host "SecureCI is ready to use." -ForegroundColor Green

Write-Host ""
Write-Host "Activate the virtual environment:"
Write-Host ""
Write-Host ".\venv\Scripts\Activate.ps1"

Write-Host ""
Write-Host "Scan a public GitHub repository:"
Write-Host ""
Write-Host "python github_scanner.py --repo-url https://github.com/USER/PROJECT.git"

Write-Host ""
Write-Host "Example:"
Write-Host ""
Write-Host "python github_scanner.py --repo-url https://github.com/pallets/flask.git"

Write-Host ""
Write-Host "============================================================"
Write-Host ""