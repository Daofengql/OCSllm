$ErrorActionPreference = 'Stop'

$compiler = Join-Path $env:WINDIR 'Microsoft.NET\Framework64\v4.0.30319\csc.exe'
if (!(Test-Path -LiteralPath $compiler)) {
    $compiler = Join-Path $env:WINDIR 'Microsoft.NET\Framework\v4.0.30319\csc.exe'
}
if (!(Test-Path -LiteralPath $compiler)) {
    throw 'Windows .NET Framework 4.8 C# compiler was not found.'
}

$release = Join-Path $PSScriptRoot 'release'
$source = Join-Path $PSScriptRoot 'src\Program.cs'
$manifest = Join-Path $PSScriptRoot 'src\app.manifest'
$icon = Join-Path $PSScriptRoot 'src\app.ico'
$exe = Join-Path $release 'OCSllm.exe'

New-Item -ItemType Directory -Force -Path $release | Out-Null
$compilerArgs = @(
    '/nologo', '/target:winexe', '/optimize+', '/platform:anycpu', '/codepage:65001',
    "/out:$exe", "/win32manifest:$manifest",
    '/reference:System.dll',
    '/reference:System.Core.dll',
    '/reference:System.Drawing.dll',
    '/reference:System.Windows.Forms.dll',
    '/reference:System.Web.Extensions.dll',
    '/reference:System.Net.Http.dll'
)
if (Test-Path -LiteralPath $icon) {
    $compilerArgs += "/win32icon:$icon"
}

& $compiler @compilerArgs $source
if ($LASTEXITCODE -ne 0) {
    throw 'C# compilation failed.'
}

$configXml = '<?xml version="1.0" encoding="utf-8"?>' + [Environment]::NewLine +
    '<configuration>' + [Environment]::NewLine +
    '  <startup>' + [Environment]::NewLine +
    '    <supportedRuntime version="v4.0" sku=".NETFramework,Version=v4.8" />' + [Environment]::NewLine +
    '  </startup>' + [Environment]::NewLine +
    '</configuration>' + [Environment]::NewLine
Set-Content -LiteralPath (Join-Path $release 'OCSllm.exe.config') -Value $configXml -Encoding UTF8

Write-Output "Build succeeded: $exe"
