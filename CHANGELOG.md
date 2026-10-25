# Changelog

## Registered package 1.0.19

Add the shared custom-app development workflow and direct project Git helper to the existing connection. Build and publish an exact commit, then install or update the private app through normal Reefy operations. Preserve app data and keep Voice speech and written readiness as separate acceptance gates. No second connection or credentials in Git configuration.

## Registered package 1.0.18

Add guided firmware update consent, verified progress and setup continuation. Keep reboot approval separate from internal-disk erasure, preserving cards, background app links and friendly names.

## Registered package 1.0.17

Restore explicit owner app links in background completion replies and mandatory storage-choice guidance. Give foreground app startup its own operation card, retaining reef names and Voice progress guidance. Add package regression coverage for both environments.

## Unreleased

- Add active Voice setup milestone speech and bounded foreground status narration, retaining event monitoring and explicit storage consent. Host audio behavior requires real-client acceptance.

- Extract shared onboarding instructions, the existing ChatGPT scaffold and package validation into the public Reefy plugins repository.
- Preserve dev/production endpoint parity and registered-package update behavior.
- Add reproducible artifact generation and CI checks. Existing installed package versions and backend contracts are unchanged.
- Document Reefy API v1 compatibility at the stable `/mcp` endpoint, separately from MCP protocol and package versions.
- Add an importable Reefy Dev workspace catalog and registered package 1.0.11, with generated-resource drift checks. Activation requires workspace admin access and verified plugin ownership.

## Friendly device naming

New-device setup honors explicit names and otherwise chooses a short reef-themed
name, avoids visible account-name collisions, preserves request identity on retries
and explains the automatic choice. Existing devices are not renamed automatically.
Later rename requests require an available authorized tool and an actual result.
