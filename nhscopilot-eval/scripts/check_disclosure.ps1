param(
    [string]$Path = "data/public"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $Path -PathType Container)) {
    throw "Public surface does not exist: $Path"
}

$files = @(Get-ChildItem -LiteralPath $Path -File -Recurse)
if ($files.Count -eq 0) {
    throw "Public surface is empty: $Path"
}

# These patterns target disclosures, not ordinary Project 09 policy wording.
$patterns = [ordered]@{
    secret = '(?i)(sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN (RSA |EC )?PRIVATE KEY-----)'
    phi = '(?i)(patient[_ -]?id|nhs[_ -]?number|date[_ -]?of[_ -]?birth|medical[_ -]?record|personally identifiable)'
    hidden_material = '(?i)(answer[_ -]?key|hidden[_ -]?label|raw[_ -]?provider|prompt[_ -]?trace|adjudication[_ -]?ledger|sealed[_ -]?evaluation)'
    restricted_text = '(?i)(BNF[_ -]?text|WHO/NHS[_ -]?code[_ -]?table|restricted[_ -]?guideline[_ -]?text|patient record)'
    unsupported_claim = '(?i)(NHS endorsed|clinically safe|clinical safety established|regulatory compliance established|best model|winner)'
}

$findings = @()
foreach ($file in $files) {
    $content = Get-Content -LiteralPath $file.FullName -Raw
    foreach ($name in $patterns.Keys) {
        if ($content -match $patterns[$name]) {
            $findings += "${name}:$($file.FullName)"
        }
    }
}

if ($findings.Count -gt 0) {
    $findings | ForEach-Object { Write-Error $_ }
    throw "Public disclosure scan failed."
}

Write-Output "PUBLIC DISCLOSURE SCAN: PASS"
Write-Output "Files scanned: $($files.Count)"
Write-Output "CPU-heavy tests/model inference/network execution: NOT USED"
