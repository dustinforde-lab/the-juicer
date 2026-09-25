<#
  The Juicer - Local Project Audit Script
  ----------------------------------------
  Run this from PowerShell in (or pointed at) your project folder.
  It does NOT modify any files. It only reads and reports.

  USAGE:
    .\audit_juicer.ps1
    .\audit_juicer.ps1 -ProjectPath "C:\Users\you\Projects\TheJuicer"

  OUTPUT:
    Creates audit_output.txt in the project folder. Paste that file's
    contents back into the chat.
#>

param(
    [string]$ProjectPath = (Get-Location).Path
)

$ExcludeDirs = @('.git', '__pycache__', 'venv', '.venv', 'env', 'node_modules', '.idea', '.vscode')
$OutFile = Join-Path $ProjectPath "audit_output.txt"

if (-not (Test-Path $ProjectPath)) {
    Write-Host "Path not found: $ProjectPath" -ForegroundColor Red
    exit 1
}

"=== JUICER PROJECT AUDIT ===" | Out-File $OutFile
"Generated: $(Get-Date)" | Out-File $OutFile -Append
"Project Path: $ProjectPath" | Out-File $OutFile -Append
"" | Out-File $OutFile -Append

function Should-Exclude($path) {
    foreach ($ex in $ExcludeDirs) {
        if ($path -match [regex]::Escape("\$ex\") -or $path -match [regex]::Escape("\$ex")) {
            return $true
        }
    }
    return $false
}

# ---- 1. Directory tree ----
"--- FOLDER STRUCTURE ---" | Out-File $OutFile -Append
Get-ChildItem -Path $ProjectPath -Recurse -File | Where-Object {
    -not (Should-Exclude $_.FullName)
} | ForEach-Object {
    $rel = $_.FullName.Substring($ProjectPath.Length)
    "$rel  ($([math]::Round($_.Length/1KB,1)) KB)" | Out-File $OutFile -Append
}
"" | Out-File $OutFile -Append

# ---- 2. Python file inventory ----
$pyFiles = Get-ChildItem -Path $ProjectPath -Recurse -Filter *.py | Where-Object {
    -not (Should-Exclude $_.FullName)
}

"--- PYTHON FILES ($($pyFiles.Count) total) ---" | Out-File $OutFile -Append
foreach ($f in $pyFiles) {
    $lines = Get-Content $f.FullName
    "$($f.FullName.Substring($ProjectPath.Length))  ($($lines.Count) lines)" | Out-File $OutFile -Append
}
"" | Out-File $OutFile -Append

# ---- 3. Per-file detail: imports, defs/classes, TODOs ----
"--- FILE DETAILS ---" | Out-File $OutFile -Append
foreach ($f in $pyFiles) {
    $rel = $f.FullName.Substring($ProjectPath.Length)
    "" | Out-File $OutFile -Append
    ">>> $rel" | Out-File $OutFile -Append

    $content = Get-Content $f.FullName

    $imports = $content | Select-String -Pattern '^\s*(import|from)\s'
    if ($imports) {
        "  IMPORTS:" | Out-File $OutFile -Append
        $imports | ForEach-Object { "    $($_.Line.Trim())" | Out-File $OutFile -Append }
    }

    $defs = $content | Select-String -Pattern '^\s*(def|class)\s'
    if ($defs) {
        "  FUNCTIONS/CLASSES:" | Out-File $OutFile -Append
        $defs | ForEach-Object { "    $($_.LineNumber): $($_.Line.Trim())" | Out-File $OutFile -Append }
    }

    $todos = $content | Select-String -Pattern 'TODO|FIXME|HACK|XXX|BROKEN'
    if ($todos) {
        "  FLAGGED COMMENTS:" | Out-File $OutFile -Append
        $todos | ForEach-Object { "    Line $($_.LineNumber): $($_.Line.Trim())" | Out-File $OutFile -Append }
    }

    $tryExcept = ($content | Select-String -Pattern '^\s*try\s*:').Count
    $exceptCount = ($content | Select-String -Pattern '^\s*except').Count
    "  Try/Except blocks: $tryExcept try / $exceptCount except" | Out-File $OutFile -Append

    $connOpens = ($content | Select-String -Pattern 'sqlite3\.connect').Count
    $withConn = ($content | Select-String -Pattern 'with\s+sqlite3\.connect').Count
    if ($connOpens -gt 0) {
        "  DB connections: $connOpens total, $withConn using 'with' (context manager)" | Out-File $OutFile -Append
        if ($withConn -lt $connOpens) {
            "  *** WARNING: possible unclosed DB connections in this file ***" | Out-File $OutFile -Append
        }
    }
}
"" | Out-File $OutFile -Append

# ---- 4. Config / requirements / env ----
"--- CONFIG & DEPENDENCIES ---" | Out-File $OutFile -Append
$configFiles = @('config.py', 'requirements.txt', '.env.example', '.env', 'setup.py', 'pyproject.toml')
foreach ($cf in $configFiles) {
    $found = Get-ChildItem -Path $ProjectPath -Recurse -Filter $cf -ErrorAction SilentlyContinue | Where-Object { -not (Should-Exclude $_.FullName) }
    foreach ($f in $found) {
        $rel = $f.FullName.Substring($ProjectPath.Length)
        "" | Out-File $OutFile -Append
        ">>> $rel" | Out-File $OutFile -Append
        if ($f.Name -ne '.env') {
            Get-Content $f.FullName | ForEach-Object { "    $_" | Out-File $OutFile -Append }
        } else {
            "    (contents skipped - may contain secrets; just confirming it exists)" | Out-File $OutFile -Append
        }
    }
}
"" | Out-File $OutFile -Append

# ---- 5. Database files ----
"--- DATABASE FILES ---" | Out-File $OutFile -Append
$dbFiles = Get-ChildItem -Path $ProjectPath -Recurse -Include *.db, *.sqlite, *.sqlite3 -ErrorAction SilentlyContinue | Where-Object { -not (Should-Exclude $_.FullName) }
if ($dbFiles) {
    foreach ($db in $dbFiles) {
        $rel = $db.FullName.Substring($ProjectPath.Length)
        "$rel  ($([math]::Round($db.Length/1KB,1)) KB, modified $($db.LastWriteTime))" | Out-File $OutFile -Append
    }
} else {
    "No .db/.sqlite files found." | Out-File $OutFile -Append
}
"" | Out-File $OutFile -Append

# ---- 6. Entry point detection ----
"--- LIKELY ENTRY POINTS ---" | Out-File $OutFile -Append
$entryCandidates = $pyFiles | Where-Object { $_.Name -match '^(app|main|home|streamlit_app)\.py$' }
foreach ($e in $entryCandidates) {
    "$($e.FullName.Substring($ProjectPath.Length))" | Out-File $OutFile -Append
}
"" | Out-File $OutFile -Append

"=== END AUDIT ===" | Out-File $OutFile -Append

Write-Host "`nAudit complete." -ForegroundColor Green
Write-Host "Report saved to: $OutFile" -ForegroundColor Green
Write-Host "Paste the contents of that file back into the chat.`n" -ForegroundColor Yellow