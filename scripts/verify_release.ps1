[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$WheelPath
)

$ErrorActionPreference = "Stop"

$wheelCandidate = $WheelPath
if (-not [System.IO.Path]::IsPathRooted($wheelCandidate)) {
    $wheelCandidate = Join-Path (Get-Location) $wheelCandidate
}
$resolvedWheel = (Resolve-Path -LiteralPath $wheelCandidate).Path
$venvPath = Join-Path ([System.IO.Path]::GetTempPath()) ("openapps-release-" + [guid]::NewGuid().ToString("N"))
$venvPython = Join-Path $venvPath "Scripts\python.exe"

try {
    & python -m venv $venvPath
    if ($LASTEXITCODE -ne 0) { throw "python -m venv failed with exit code $LASTEXITCODE" }

    & $venvPython -m pip install --no-index --no-deps $resolvedWheel
    if ($LASTEXITCODE -ne 0) { throw "wheel installation failed with exit code $LASTEXITCODE" }

    & $venvPython -c "import openapps; assert openapps.__version__ == '0.2.0'; print('Installed OpenApps', openapps.__version__)"
    if ($LASTEXITCODE -ne 0) { throw "installed package version check failed with exit code $LASTEXITCODE" }

    & $venvPython -m openapps doctor
    if ($LASTEXITCODE -ne 0) { throw "doctor failed with exit code $LASTEXITCODE" }

    & $venvPython -m openapps replace notion
    if ($LASTEXITCODE -ne 0) { throw "replace smoke test failed with exit code $LASTEXITCODE" }

    Write-Output "Release verification passed: $resolvedWheel"
}
finally {
    if (Test-Path -LiteralPath $venvPath) {
        Remove-Item -LiteralPath $venvPath -Recurse -Force
    }
}
