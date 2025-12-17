param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

switch ($Command) {
    "lint-check" {
        Write-Host "Running ruff check..." -ForegroundColor Yellow
        python -m ruff check .
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

        Write-Host "Running ruff format check..." -ForegroundColor Yellow
        python -m ruff format . --check
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

        Write-Host "Lint check passed!" -ForegroundColor Green
    }
    "lint-fix" {
        Write-Host "Running ruff check with fixes..." -ForegroundColor Yellow
        python -m ruff check . --fix
        python -m ruff format .
        Write-Host "Lint fixes applied!" -ForegroundColor Green
    }
    "install" {
        Write-Host "Installing dependencies..." -ForegroundColor Yellow
        pip install -r requirements.txt
        pip install ruff
        Write-Host "Dependencies installed!" -ForegroundColor Green
    }
    default {
        Write-Host "Available commands:" -ForegroundColor Cyan
        Write-Host "  .\make.ps1 lint-check  - Check code style"
        Write-Host "  .\make.ps1 lint-fix    - Fix code style"
        Write-Host "  .\make.ps1 install     - Install dependencies"
    }
}
