# Store a newly issued Mealie QA token with Windows DPAPI encryption.
# No token literal is stored in this script or inside the Git repository.
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
if ($env:OS -ne 'Windows_NT') {
    throw 'Script nay chi ho tro Windows (DPAPI cua tai khoan Windows).'
}

$privateDir = Join-Path $env:APPDATA 'MealieQA'
$secretPath = Join-Path $privateDir 'mealie-token.clixml'
New-Item -Path $privateDir -ItemType Directory -Force | Out-Null

if (Test-Path -LiteralPath $secretPath) {
    $choice = Read-Host 'Da co token duoc luu. Ghi de bang token MOI? (Y/N)'
    if ($choice -notin @('Y', 'y')) { Write-Host 'Khong thay doi token.'; exit 0 }
}

Write-Host 'Nhap token QA MOI (da thu hoi token cu neu da lo). Noi dung nhap duoc an.'
$secureToken = Read-Host 'Mealie QA Token' -AsSecureString
try {
    $secureToken | Export-Clixml -LiteralPath $secretPath
    Write-Host 'Da luu token duoi dang ma hoa DPAPI, chi tai khoan Windows nay tren may nay co the nap lai.'
    Write-Host 'Khong di chuyen file token vao Git repo hoac chia se token trong chat.'
} finally {
    Remove-Variable secureToken -ErrorAction SilentlyContinue
}
