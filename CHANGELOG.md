# Changelog

## Unreleased

- Add active Voice setup milestone speech and bounded foreground status narration, retaining event monitoring and explicit storage consent. Host audio behavior requires real-client acceptance.

- Extract shared onboarding instructions, the existing ChatGPT scaffold and package validation into the public Reefy plugins repository.
- Preserve dev/production endpoint parity and registered-package update behavior.
- Add reproducible artifact generation and CI checks. Existing installed package versions and backend contracts are unchanged.
- Document Reefy API v1 compatibility at the stable `/mcp` endpoint, separately from MCP protocol and package versions.
- Add an importable Reefy Dev workspace catalog and registered package 1.0.11, with generated-resource drift checks. Activation requires workspace admin access and verified plugin ownership.
