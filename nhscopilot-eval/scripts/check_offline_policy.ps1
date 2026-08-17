$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$required = @(
    "configs\benchmark.yaml",
    "configs\execution.yaml",
    "configs\source_manifest.yaml",
    "configs\rights_ledger.yaml",
    "configs\models.yaml",
    "src\nhscopilot_eval\contracts.py",
    "tests\test_contracts.py"
)

foreach ($relativePath in $required) {
    $absolutePath = Join-Path $root $relativePath
    if (-not (Test-Path -LiteralPath $absolutePath)) {
        throw "Missing required local policy file: $relativePath"
    }
}
Write-Output "PASS files: $($required.Count) local policy files exist"

$execution = Get-Content -Raw -LiteralPath (Join-Path $root "configs\execution.yaml")
foreach ($marker in @(
    'execution_policy: "offline_first"',
    'provider_calls: "disabled"',
    'network_access: "disabled"',
    'local_model_downloads: "disabled"',
    'allow_remote: false'
)) {
    if (-not $execution.Contains($marker)) {
        throw "Missing offline execution marker: $marker"
    }
}
Write-Output "PASS execution: offline, no-provider, and no-download policy is present"

$rights = Get-Content -Raw -LiteralPath (Join-Path $root "configs\rights_ledger.yaml")
foreach ($marker in @(
    'status: "synthetic_fallback_active"',
    'external_source_access: "blocked"',
    'restricted_content_access: "not_performed"',
    'public_release: "blocked_until_disclosure_review"',
    'source_url: null'
)) {
    if (-not $rights.Contains($marker)) {
        throw "Missing rights marker: $marker"
    }
}
if ($rights -match '(?i)https?://') {
    throw "External URL found in the local rights ledger"
}
Write-Output "PASS rights: synthetic fallback is active and no external URL is admitted"

$models = Get-Content -Raw -LiteralPath (Join-Path $root "configs\models.yaml")
foreach ($marker in @(
    'exact_snapshot_required: true',
    'availability_verification_required: true',
    'silent_substitution: false',
    'unavailable_state: "not_run"',
    'model_training: "out_of_scope"',
    'gpu_notebook_role: "optional_evaluation_only"',
    'availability_verified: false'
)) {
    if (-not $models.Contains($marker)) {
        throw "Missing model registry marker: $marker"
    }
}
if ($models -match 'status: "available"') {
    throw "Unverified available model state found"
}
Write-Output "PASS models: no model availability, training, or quality claim is fabricated"

$dataFiles = @(Get-ChildItem -LiteralPath $root -Recurse -File | Where-Object {
    $extension = $_.Extension.ToLowerInvariant()
    $extension -in @(".parquet", ".sqlite", ".db", ".log") -or
        ($extension -eq ".pyc" -and $_.FullName -notmatch "[\\]__pycache__[\\]")
})
if ($dataFiles.Count -gt 0) {
    throw "Forbidden generated artifact found: $($dataFiles.FullName -join ', ')"
}
$jsonlFiles = @(Get-ChildItem -LiteralPath $root -Recurse -File -Filter *.jsonl)
$unexpectedJsonl = @($jsonlFiles | Where-Object {
    $_.FullName -notmatch ([regex]::Escape((Join-Path $root "data")) + "[\\](private|public|sealed)[\\]")
})
if ($unexpectedJsonl.Count -gt 0) {
    throw "JSONL artifact outside an approved local data boundary: $($unexpectedJsonl.FullName -join ', ')"
}
Write-Output "PASS boundary: local JSONL is confined to data/private, data/public, or data/sealed; no databases, logs, or unignored bytecode artifacts exist"

$sourceText = (Get-ChildItem -LiteralPath $root -Recurse -File | Where-Object {
    $_.FullName -notmatch "[\\]__pycache__[\\]"
} | ForEach-Object {
    Get-Content -Raw -LiteralPath $_.FullName
}) -join "`n"
if ($sourceText -match '(?i)(sk-[A-Za-z0-9]{12,}|api[_-]?key\s*[:=]\s*["''][^"'']+["'']|gsk_[A-Za-z0-9_-]{12,})') {
    throw "Secret-like value found in local source boundary"
}
if ($sourceText -match '(?i)Claude\s+leads|GPT-4o\s+leads|winner\s*[:=]') {
    throw "Directional result claim found in local source boundary"
}
Write-Output "PASS disclosure: no secret-like values or directional result claims found"
Write-Output "OFFLINE POLICY CHECK: PASS"
Write-Output "CPU-heavy tests/model inference/network execution: NOT USED"
