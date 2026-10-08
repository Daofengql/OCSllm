# Usage

## Configure sources

Right-click the tray icon and choose “打开配置”. The main window contains the source list, status, and three actions:

- **保存配置** saves the current source list and settings.
- **复制 OCS 配置** copies the generated `ocs-answerer-wrapper.json` content.
- **测试模型** sends a small sample question to the active source.

Source list actions:

- Double-click a row to activate that source.
- Right-click “新增源” to create a source in a dialog.
- Right-click “修改 / 重命名” to edit the source or its name in a dialog.
- Right-click “删除源” to remove a source; at least one source is kept.

Each source keeps its own success and failure counters.

## Import into OCS

Start OCSllm, click “复制 OCS 配置”, and import the clipboard JSON into the OCS answerer settings. OCS sends requests to:

```text
POST http://127.0.0.1:8765/answer
```

The bridge forwards each request to the active source through the OpenAI Responses API.

## Network and retries

The remote source must be compatible with the Responses API. HTTPS is the default and is recommended. For a trusted proxy without HTTPS, enable “允许远程 HTTP（无 HTTPS 代理）” for that source and use an `http://.../v1` base URL. Timeouts, connection failures, 429, and 5xx responses are retried up to three times before the request is reported as failed.

## Command-line switches

The executable accepts the following optional switches:

- `--config <path>` loads a configuration file from the specified path.
- `--headless` runs the local bridge without the tray UI.
- `--show-settings` opens the settings window when the tray app starts.

For automation, start with `--headless --config <path>` and poll `GET /healthz` before sending questions.

## Troubleshooting

- Open `http://127.0.0.1:8765/healthz` to check whether the bridge is running.
- Check the active source's base URL, model, and API key in the configuration window.
- If the port is busy, edit `release/config.json`, restart OCSllm, and import a new OCS configuration.
- Runtime diagnostics are written to `release/service.log`; API keys are not written to the log.
- If an existing configuration enables remote HTTP, review it before sharing the file. New sources default to HTTPS-only.
