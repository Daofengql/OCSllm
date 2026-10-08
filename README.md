# OCSllm

[![Build](https://github.com/Daofengql/OCSllm/actions/workflows/build.yml/badge.svg)](https://github.com/Daofengql/OCSllm/actions/workflows/build.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A Windows tray application that bridges OCS with the OpenAI Responses API. OCS talks to a local endpoint, while the active backend source sends questions to a configured remote model. The project supports multiple sources, HTTPS, and trusted HTTP proxies.

## Features

- Runs in the Windows notification area and exposes `http://127.0.0.1:8765/answer`.
- Uses the OpenAI Responses API; it does not use a local question bank or local model.
- Supports multiple backend sources. Each source has its own name, API key, base URL, model, and success/failure counters.
- Double-click a source to activate it. Right-click to add, edit, rename, or remove a source.
- Retries timeouts, network failures, HTTP 429, and 5xx responses up to three times.
- Uses HTTPS by default; trusted `http://` proxy endpoints can be enabled per source.
- Copies a ready-to-import OCS configuration to the clipboard.

## Project layout

```text
├─ README.md                         Project overview
├─ LICENSE                           MIT license
├─ .gitignore                        Local secrets and runtime files
├─ build.ps1                         .NET Framework build script
├─ src/
│  ├─ Program.cs                     Application source
│  ├─ app.manifest                   Windows manifest
│  └─ app.ico                        Tray and window icon
├─ tools/
│  └─ make_icon.py                   Optional icon generator
├─ examples/
│  └─ config.example.json            Sanitized configuration example
├─ docs/
│  └─ usage.md                       User guide
├─ .github/
│  ├─ workflows/build.yml            Windows CI build
│  └─ ISSUE_TEMPLATE/                 Issue templates
├─ CHANGELOG.md                       Release history
├─ CONTRIBUTING.md                    Contribution guide
├─ SECURITY.md                        Security policy
└─ release/
   ├─ OCSllm.exe                     Build output
   ├─ OCSllm.exe.config
   └─ config.json                     Local configuration, ignored by Git
```

## Build

Requirements: Windows and .NET Framework 4.8. Run this from the project root:

```powershell
.\build.ps1
```

The executable is written to `release/`. For a new installation, copy `examples/config.example.json` to `release/config.json` and fill in your own API key, base URL, and model. Keep a real `config.json` local; never commit it to a public repository.

The build uses the C# compiler included with Windows .NET Framework tooling. GitHub Actions runs the same PowerShell build on every push and pull request.

## Run and configure

Double-click `release/OCSllm.exe`. The program stays in the notification area. Right-click the tray icon and choose “打开配置”:

1. Double-click a source to activate it.
2. Right-click a source to add, edit/rename, or remove it.
3. Use “保存配置” to save settings and “测试模型” to test the active source.
4. Use “复制 OCS 配置” and import the clipboard JSON into OCS.

OCS uses `http://127.0.0.1:8765/answer`. If you change the port, copy and import the OCS configuration again.

The executable also supports these optional switches:

- `--config <path>` uses a configuration file outside `release/`.
- `--headless` starts the local bridge without opening the tray UI.
- `--show-settings` opens the configuration window on startup.

## HTTP proxies

A source can use an OpenAI-compatible HTTPS endpoint such as `https://api.openai.com/v1` or a trusted HTTP proxy such as `http://127.0.0.1:8080/v1`. Enable “允许远程 HTTP（无 HTTPS 代理）” for an HTTP source. HTTP sends the API key and question content in plaintext, so use it only with a trusted local or private proxy.

## Runtime files

The executable reads `config.json` from its own directory and writes `ocs-answerer-wrapper.json` and `service.log` there. These runtime files and local secrets are ignored by Git.

## Health check

When the program is running, open:

```text
http://127.0.0.1:8765/healthz
```

A successful response means the local bridge is ready.

## Local API

`GET /healthz` returns service status and request counters. `POST /answer` accepts the OCS question JSON and requires the `X-OCS-Token` header from the generated wrapper. The bridge binds only to loopback and never exposes a public listener.

## Contributing and security

See [CONTRIBUTING.md](CONTRIBUTING.md) for the development workflow and [SECURITY.md](SECURITY.md) for reporting guidance. See [CHANGELOG.md](CHANGELOG.md) for release history.

## License

MIT License. See [LICENSE](LICENSE).
