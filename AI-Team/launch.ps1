param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidateSet("enable", "carry", "validate", "status", "merge")]
    [string]$Command,

    [Parameter(Position = 1)]
    [string]$OtherPath
)

$ErrorActionPreference = "Stop"
$Utf8 = New-Object System.Text.UTF8Encoding($false)
[Console]::OutputEncoding = $Utf8
$OutputEncoding = $Utf8

function Fail([string]$Message) {
    [Console]::Error.WriteLine($Message)
    exit 1
}

try {
    $capsuleRoot = [System.IO.Path]::GetFullPath((Split-Path -Parent $PSScriptRoot))
    $configName = "Python" + [string][char]0x8DEF + [string][char]0x5F84 + ".txt"
    $configPath = Join-Path $capsuleRoot $configName
    if (-not (Test-Path -LiteralPath $configPath -PathType Leaf)) {
        Fail "缺少 Python路径.txt。请在胶囊根目录创建该文件，并填写 Python 可执行文件的绝对路径。"
    }

    $text = [System.IO.File]::ReadAllText($configPath, [System.Text.Encoding]::UTF8)
    $pythonPath = $null
    $doubleOpen = [string][char]0x201C
    $doubleClose = [string][char]0x201D
    $singleOpen = [string][char]0x2018
    $singleClose = [string][char]0x2019
    foreach ($line in ($text -split "`r?`n")) {
        $candidate = ($line -replace "[\u200E\u200F\u202A-\u202E\u2066-\u2069\uFEFF]", "").Trim()
        if ([string]::IsNullOrWhiteSpace($candidate)) { continue }
        if ($candidate.Length -ge 2) {
            $first = $candidate.Substring(0, 1)
            $last = $candidate.Substring($candidate.Length - 1, 1)
            if (($first -eq '"' -and $last -eq '"') -or ($first -eq "'" -and $last -eq "'") -or ($first -eq $doubleOpen -and $last -eq $doubleClose) -or ($first -eq $singleOpen -and $last -eq $singleClose)) {
                $candidate = $candidate.Substring(1, $candidate.Length - 2).Trim()
            }
        }
        $pythonPath = $candidate
        break
    }

    if ([string]::IsNullOrWhiteSpace($pythonPath) -or -not [System.IO.Path]::IsPathRooted($pythonPath)) {
        Fail "Python路径.txt 中没有有效的绝对路径。请填写 Python 可执行文件的完整路径。"
    }
    $pythonPath = [System.IO.Path]::GetFullPath($pythonPath)
    if (-not (Test-Path -LiteralPath $pythonPath -PathType Leaf)) {
        Fail ("Python 路径不存在: " + $pythonPath + "。请修改胶囊根目录的 Python路径.txt。")
    }

    & $pythonPath -c "import sys; raise SystemExit(0 if sys.version_info.major == 3 else 1)" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Fail ("配置的程序不是可用的 Python 3: " + $pythonPath)
    }

    $script = Join-Path $PSScriptRoot "capsule.py"
    if ($OtherPath) {
        & $pythonPath $script $Command --python $pythonPath --other $OtherPath
    } else {
        & $pythonPath $script $Command --python $pythonPath
    }
    exit $LASTEXITCODE
}
catch {
    Fail ("启动团队胶囊失败: " + $_.Exception.Message + " [line " + $_.InvocationInfo.ScriptLineNumber + "]")
}
