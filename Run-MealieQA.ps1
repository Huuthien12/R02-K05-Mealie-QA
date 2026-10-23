# Run pytest with a Mealie QA token decrypted locally for this process only.
# Usage:
#   .\Run-MealieQA.ps1
#   .\Run-MealieQA.ps1 -Mode Expansion -ConfirmDisposableQA
#   .\Run-MealieQA.ps1 -Mode All -ConfirmDisposableQA
# Requires Windows + the DPAPI token saved by Save-MealieQAToken.ps1.
[CmdletBinding()]
param(
    [ValidateSet('P0', 'Expansion', 'All')]
    [string]$Mode = 'P0',
    [switch]$ConfirmDisposableQA,
    [string]$BaseUrl = 'http://localhost:9091'
)

$ErrorActionPreference = 'Stop'
if ($env:OS -ne 'Windows_NT') { throw 'Can Windows de doc token DPAPI.' }

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Join-Path $repoRoot '.venv\Scripts\python.exe'
$secretPath = Join-Path (Join-Path $env:APPDATA 'MealieQA') 'mealie-token.clixml'
$reports = Join-Path $repoRoot 'reports\local-runs'

if (-not (Test-Path -LiteralPath $python)) { throw "Khong thay Python venv: $python" }
if (-not (Test-Path -LiteralPath $secretPath)) {
    throw 'Chua co token DPAPI. Chay .\Save-MealieQAToken.ps1 truoc.'
}
if ($Mode -in @('Expansion','All') -and -not $ConfirmDisposableQA) {
    throw 'P1 co write/delete. Chi chay tren QA DU LIEU TAM va them -ConfirmDisposableQA.'
}

$BaseUrl = $BaseUrl.TrimEnd('/')
if ($BaseUrl -notin @('http://localhost:9091', 'http://127.0.0.1:9091')) {
    throw 'Script chi cho phep Mealie QA local tai localhost:9091 / 127.0.0.1:9091.'
}

Write-Host 'Kiem tra Mealie local va OpenAPI...'
foreach ($endpoint in @('/api/app/about', '/openapi.json')) {
    $reply = Invoke-WebRequest -Uri ($BaseUrl + $endpoint) -UseBasicParsing -TimeoutSec 20
    if ([int]$reply.StatusCode -ne 200) { throw "Endpoint $endpoint khong tra 200." }
}

$secure = Import-Clixml -LiteralPath $secretPath
if (-not ($secure -is [System.Security.SecureString])) {
    throw 'File token khong dung dinh dang SecureString DPAPI.'
}
try {
    $plain = [System.Net.NetworkCredential]::new('qa', $secure).Password
    $env:MEALIE_API_TOKEN = $plain
    $env:MEALIE_BASE_URL = $BaseUrl
    Remove-Variable plain -ErrorAction SilentlyContinue

    # An authenticated, read-only check before pytest, without printing the token.
    $authReply = Invoke-WebRequest -Uri ($BaseUrl + '/api/users/self') -Headers @{
        Authorization = 'Bearer ' + $env:MEALIE_API_TOKEN
    } -UseBasicParsing -TimeoutSec 20
    if ([int]$authReply.StatusCode -ne 200) {
        throw 'Token QA khong duoc chap nhan (GET /api/users/self).'
    }
    Write-Host 'Mealie va token QA OK. Chi ghi JUnit/log, khong ghi token.'
    New-Item -Path $reports -ItemType Directory -Force | Out-Null
    $stamp = Get-Date -Format 'yyyyMMdd-HHmmss-fff'

    if ($Mode -in @('P0', 'All')) {
        $p0Files = @(
            'tests/schemathesis/test_p0_selection.py',
            'tests/schemathesis/test_p0_collections.py',
            'tests/schemathesis/test_p0_details.py',
            'tests/schemathesis/test_p0_smoke.py'
        )
        $p0Xml = Join-Path $reports "p0-$stamp.xml"
        Write-Host 'Dang chay P0 read-only (known defect co the khien pytest exit 1)...'
        Push-Location $repoRoot
        try {
            & $python -m pytest @p0Files -q -rs "--junitxml=$p0Xml"
            $p0Exit = $LASTEXITCODE
        } finally { Pop-Location }
        Write-Host "P0 exit code: $p0Exit; JUnit: $p0Xml"
        if ($p0Exit -ge 2) { throw 'P0 bi loi thuc thi/thu thap. Dung truoc khi chay P1.' }
    }

    if ($Mode -in @('Expansion', 'All')) {
        Write-Warning 'Ban da xac nhan dang dung QA instance rieng voi DU LIEU TAM co the xoa. P1 se POST/PUT/PATCH/DELETE.'
        $expansionFiles = @(
            'tests/schemathesis/test_tc22_tc25_shopping_lists.py',
            'tests/schemathesis/test_tc26_tc29_mealplans.py',
            'tests/schemathesis/test_tc30_tc33_shopping_items.py',
            'tests/schemathesis/test_tc34_tc37_recipes.py'
        )
        $expXml = Join-Path $reports "tc22-tc37-$stamp.xml"
        $env:MEALIE_RUN_P1_EXPANSION = '1'
        Push-Location $repoRoot
        try {
            & $python -m pytest @expansionFiles -q -rs "--junitxml=$expXml"
            $expExit = $LASTEXITCODE
        } finally { Pop-Location }
        Write-Host "TC22-TC37 exit code: $expExit; JUnit: $expXml"
        if ($expExit -ne 0) {
            Write-Warning 'Co the co FAIL/SKIP. Xem JUnit va phan loai, KHONG sua expected chi de PASS.'
        }
    }
} finally {
    Remove-Item Env:\MEALIE_API_TOKEN -ErrorAction SilentlyContinue
    Remove-Item Env:\MEALIE_BASE_URL -ErrorAction SilentlyContinue
    Remove-Item Env:\MEALIE_RUN_P1_EXPANSION -ErrorAction SilentlyContinue
    Remove-Variable secure -ErrorAction SilentlyContinue
    Write-Host 'Da go cac bien token/gate khoi process PowerShell dang chay.'
}
