# Changelog

## Unreleased

- Before adoption, obtain an explicit internal-storage decision. Send `preserve_internal_storage:true` only after preservation consent; handle a missing-choice refusal by asking instead of retrying silently.

- Make the internal SSD the recommended new-device setup choice in text and voice, with an explicit exact-disk erase-or-preserve decision before adoption. Generic setup consent never authorizes erasure.

- Extract shared onboarding instructions, the existing ChatGPT scaffold and package validation into the public Reefy plugins repository.
- Preserve dev/production endpoint parity and registered-package update behavior.
- Add reproducible artifact generation and CI checks. Existing installed package versions and backend contracts are unchanged.
- Document Reefy API v1 compatibility at the stable `/mcp` endpoint, separately from MCP protocol and package versions.
- Add an importable Reefy Dev workspace catalog and registered package 1.0.11, with generated-resource drift checks. Activation requires workspace admin access and verified plugin ownership.
