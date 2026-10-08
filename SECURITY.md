# Security policy

## Supported versions

The latest `main` branch is the supported version.

## Reporting a vulnerability

Please use GitHub's private vulnerability reporting for this repository when available. If it is unavailable, open an issue without credentials or proof-of-concept secrets and ask for a private contact channel.

Never include API keys, local tokens, private proxy URLs, or unredacted logs in a public issue.

## Security notes

- The bridge binds to loopback (`127.0.0.1`) and requires the generated `X-OCS-Token` header for answer requests.
- HTTPS is the default for remote model endpoints. Remote HTTP must be enabled per source and should only be used with a trusted private proxy.
- `config.json`, logs, and generated wrappers are local runtime files and are ignored by Git.
