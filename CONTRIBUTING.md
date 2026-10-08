# Contributing

Thanks for helping improve OCSllm.

## Development setup

OCSllm is a Windows tray application built with the .NET Framework 4.8 compiler that ships with Windows. No package manager or external runtime dependency is required.

1. Clone the repository.
2. Run `.\build.ps1` from the repository root in PowerShell.
3. Copy `examples\config.example.json` to `release\config.json` and fill in a test API key locally.
4. Run `release\OCSllm.exe` and verify `/healthz` and the OCS wrapper flow.

Keep API keys, local configuration, logs, and compiled binaries out of commits. The repository `.gitignore` already covers the normal files.

## Pull requests

- Keep changes focused and explain the user-visible behavior.
- Update `README.md`, `docs/usage.md`, or `CHANGELOG.md` when behavior or configuration changes.
- Run `.\build.ps1` before opening a pull request.
- Do not include real API keys, private endpoints, or personal configuration files.

## Reporting bugs

Include the Windows version, build date, steps to reproduce, and a redacted excerpt from `release\service.log`. Replace API keys and local tokens with `[redacted]` before sharing logs.
