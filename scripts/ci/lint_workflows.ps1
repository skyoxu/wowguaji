$ErrorActionPreference = 'Stop'

function Test-WorkflowFile($path) {
  $errors = @()
  $lines = Get-Content -Encoding UTF8 $path
  $first = ($lines | Where-Object { $_.Trim() -ne '' -and -not ($_.Trim().StartsWith('#')) } | Select-Object -First 1)
  if (-not $first -or ($first -notmatch '^name:')) { $errors += "missing or misplaced 'name:' at file start" }
  if (-not ($lines -match '^on:')) { $errors += "missing 'on:' block" }
  if (-not ($lines -match '^jobs:')) { $errors += "missing 'jobs:' block" }

  $runsOnLines = @()
  for ($i=0; $i -lt $lines.Count; $i++) {
    $l = $lines[$i]
    if ($l -match '^\s+runs-on:\s*(.+?)\s*$') {
      $runsOnLines += @{ Line = $i + 1; Value = $matches[1].Trim().Trim('"').Trim("'") }
    }
  }
  if ($runsOnLines.Count -eq 0) {
    $errors += "missing 'runs-on: windows-latest' in jobs"
  } else {
    foreach ($ro in $runsOnLines) {
      if ($ro.Value -ne 'windows-latest') { $errors += "non-windows runner detected (line $($ro.Line)): runs-on: $($ro.Value)" }
    }
  }

  $shellLines = @()
  for ($i=0; $i -lt $lines.Count; $i++) {
    $l = $lines[$i]
    if ($l -match '^\s+shell:\s*(.+?)\s*$') {
      $shellLines += @{ Line = $i + 1; Value = $matches[1].Trim().Trim('"').Trim("'") }
    }
  }
  foreach ($sh in $shellLines) {
    if ($sh.Value -ne 'pwsh') { $errors += "non-pwsh shell detected (line $($sh.Line)): shell: $($sh.Value)" }
  }
  if (($lines -match '^\s+run:\s*') -and -not ($lines -match '^\s+shell:\s*pwsh\s*$')) {
    $errors += "missing 'shell: pwsh' for run steps (require explicit shell per step or job-level defaults)"
  }

  for ($i=0; $i -lt $lines.Count; $i++) {
    $l = $lines[$i]
    if ($l -match '^\s+with:\s*$') {
      $hasUses = $false; $usesSetupDotnet = $false
      for ($j=$i-1; $j -ge [Math]::Max(0,$i-6); $j--) {
        $pl = $lines[$j]
        if ($pl -match '^\s+uses:\s*(.+)$') { $hasUses = $true; if ($pl -match 'actions/setup-dotnet') { $usesSetupDotnet = $true }; break }
        if ($pl -match '^\s*-\s+name:') { break }
      }
      if (-not $hasUses) { $errors += "orphan 'with:' not associated to a 'uses:' step (line $($i+1))" }
      if (($i+1) -lt $lines.Count) {
        $next = $lines[$i+1]
        if ($next -match '^\s+dotnet-version:' -and -not $usesSetupDotnet) { $errors += "'dotnet-version' found under non-setup-dotnet step (line $($i+2))" }
      }
    }
  }
  return ,$errors
}

$wfDir = Join-Path (Join-Path $PSScriptRoot '../..') '.github/workflows'
if (-not (Test-Path $wfDir)) { Write-Error "Workflows folder not found: $wfDir" }

$failed = 0
Get-ChildItem $wfDir -Filter *.yml | ForEach-Object {
  $errs = Test-WorkflowFile $_.FullName
  if ($errs.Count -gt 0) {
    Write-Warning "$($_.Name):"; foreach ($e in $errs) { Write-Warning "  - $e" }; $failed++
  } else { Write-Host "OK  $($_.Name)" }
}

if ($failed -gt 0) { Write-Error "Workflow lint found $failed file(s) with issues." } else { Write-Host 'All workflows look sane.' }

