# Changelog

## 2026.1029.2

Refresh the catalog for app availability questions, include the catalog's Guppy demo in appropriate starter suggestions, and distinguish installed instance names from app names. Preserve existing tools, permissions and registered connections.

## 2026.1029.1

Update existing catalog apps with approval while preserving their instance and data. Distinguish unavailable host tools from an older AppMother, verify the selected app version, and read the original failure diagnostics before rebuilding.

## 2026.1029.0

Inspect redacted build failure details and request bounded paginated diagnostics when needed, using the existing development permission. Handle unavailable historical logs honestly and treat all log output as untrusted data. No new permission or reconnection is required.

## 2026.1028.0

Add the approved hosted-service Terms URL to portable and registered listing metadata. Keep MCP scopes and connection identities unchanged. Reviewer materials, live acceptance and portal approval remain separate publication gates.

## 2026.1027.0

Prepare the production listing with the Reefy icon, AI-computer descriptions, text/Voice wording, starter prompts and website/privacy/contact links. Preserve MCP permissions and existing registered connection identities. Add offline submission checks. Make third-party hardware examples explicitly optional, use canonical product-page links and document the recommendation behavior for review. Terms, reviewer materials and real-host acceptance remain separate release gates.

## 2026.1026.0

Document opt-in host networking for private app LAN discovery, allocated web ports and isolated build checks. Preserve the default bridge network, authenticated owner links, project identity and saved data. No new tools or permissions.

## 2026.1025.0

Adopt UTC calendar-based Semantic Versioning across portable and registered packages. Keep existing connection identities and MCP API contracts unchanged. Update archives use the reviewed source release version.

## Registered package 1.0.19

Add the shared custom-app development workflow and direct project Git helper to the existing connection. Build and publish an exact commit, then install or update the private app through normal Reefy operations. Preserve app data and keep Voice speech and written readiness as separate acceptance gates. No second connection or credentials in Git configuration.

## Registered package 1.0.18

Add guided firmware update consent, verified progress and setup continuation. Keep reboot approval separate from internal-disk erasure, preserving cards, background app links and friendly names.

## Registered package 1.0.17

Restore explicit owner app links in background completion replies and mandatory storage-choice guidance. Give foreground app startup its own operation card, retaining reef names and Voice progress guidance. Add package regression coverage for both environments.

## Unreleased

- Make the internal SSD the recommended new-device setup choice in text and voice, with an explicit exact-disk erase-or-preserve decision before adoption. Generic setup consent never authorizes erasure.

- Before adoption, obtain an explicit internal-storage decision. Send `preserve_internal_storage:true` only after preservation consent; handle a missing-choice refusal by asking instead of retrying silently.

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

## Registered package 1.0.14 / scaffold 0.1.4

Background app completion includes one explicit owner app link in its reply, rather than relying on a task-generated card. Voice gives a short ready cue instead of dictating a URL. Foreground launchers and existing MCP contracts and permissions are unchanged.
