param (
    [Parameter(Mandatory=$true)]
    [string]$RollNo,

    [Parameter(Mandatory=$true)]
    [string]$Name
)

$CleanName = $Name -replace '\s+', '_'
$ZipFileName = "${RollNo}_${CleanName}_Code.zip"
$Destination = Join-Path -Path (Get-Location) -ChildPath $ZipFileName

Write-Host "Packaging AI Career Roadmap submission for $Name ($RollNo)..." -ForegroundColor Cyan

# Files to package
$FilesToZip = @(
    "app.py",
    "index.html",
    "AI_Career_Roadmap.ipynb",
    "requirements.txt",
    ".env.example",
    ".gitignore",
    "README.md"
)

$ExistingFiles = $FilesToZip | Where-Object { Test-Path $_ }

$TempFolder = Join-Path -Path $env:TEMP -ChildPath "Submission_${RollNo}_Roadmap"
if (Test-Path $TempFolder) { Remove-Item -Recurse -Force $TempFolder }
New-Item -ItemType Directory -Path $TempFolder | Out-Null

foreach ($f in $ExistingFiles) {
    Copy-Item $f -Destination $TempFolder
}

if (Test-Path $Destination) { Remove-Item -Force $Destination }

Compress-Archive -Path "$TempFolder\*" -DestinationPath $Destination -Force
Remove-Item -Recurse -Force $TempFolder

Write-Host "SUCCESS! Submission archive created at: $Destination" -ForegroundColor Green
Write-Host "Security Check: .env was safely excluded." -ForegroundColor Yellow
