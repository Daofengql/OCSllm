# Changelog

All notable changes to OCSllm are documented here.

## [1.1.0] - 2026-10-08

- Added per-source protocol selection for OpenAI Responses, OpenAI Chat Completions, and Claude Messages.
- Added protocol-aware authentication, request payloads, response parsing, and endpoint paths.
- Base URLs can omit `/v1`; the selected protocol supplies the final API path.

## [1.0.0] - 2026-10-08

- Initial public release.
- Added a Windows tray bridge for the OpenAI Responses API.
- Added multiple backend sources with per-source counters.
- Added local token authentication, retries, request limits, and a health endpoint.
- Added a PowerShell build script and a sanitized configuration example.
