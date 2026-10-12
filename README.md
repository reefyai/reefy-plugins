# Reefy plugins

Shared onboarding skills and assistant packages for Reefy. The hosted Reefy service provides OAuth, account authorization, MCP tools, events and device control. This repository contains the distributable instructions and connection configuration, not a second backend.

## Source layout

- `shared/skills/`: authoritative workflow instructions.
- `shared/docs/`: shared onboarding and golden journey.
- `providers/chatgpt/plugin/`: existing portable ChatGPT manifest and MCP configuration.
- `providers/claude/` and `providers/grok/`: integration status and future provider adapters.
- `package.py`: shared renderer and existing registered-package update helper.
- `tests/`: synthetic package validation and distribution regressions.
- `tools/build.py`: repository automation producing reproducible package ZIPs and checksums.

Dev and production use the same workflow, tool contracts and `/mcp` path. Only trusted deployment configuration and environment-owned identities differ. Claude and Grok distribution is not implemented yet; presence of a provider folder does not imply host support.

## Development

Use Python 3.12 or newer. Install `pytest`, then run `python -m pytest -q`. Run `python tools/build.py` to generate the dev and production portable scaffolds in `dist/`. CI runs the same checks and retains the artifacts with the exact source revision and SHA-256 checksums. The portable scaffold keeps its existing version; this repository move does not publish a new installed plugin version.

The package is readable by its recipients. Never commit credentials, personalized boot images, reviewer access instructions, account data, device identities or live-test transcripts. Keep credentials in the secure submission portal, outside the distributed package.

## Distribution status

Portable packages are scaffolds, not approved public directory releases. They need publisher metadata, host registration, live testing and OpenAI review before public publication. Existing private registered ChatGPT packages use their downloaded `.app.json` mapping. The update helper preserves that identity and avoids adding a duplicate direct MCP connection. Supply the downloaded package privately; no real registered mapping is committed here.

Publishing this repository does not update the existing Reefy Dev installation, import a workspace marketplace or submit a public plugin. Those distribution steps have their own validation gates.

## Backend compatibility

Packages connect to the hosted Reefy MCP API. Validate package compatibility against the connected deployment before release. Authorization is enforced by Reefy independently of the skills. This repository does not expose or prescribe the hosted service implementation.

See [MCP compatibility policy](docs/mcp-compatibility.md), [release practices](docs/releases.md) and [the golden journey](shared/docs/golden-user-journey.md).

## GitHub workspace catalog

The root `.agents/plugins/marketplace.json` references the complete registered Reefy Dev bundle in `plugins/reefy-dev/`. Shared instructions stay authoritative under `shared/`; run `python tools/sync_workspace.py` after changing them. CI rejects drift in the generated bundle. The only published connection identifiers are non-secret plugin/app references. They grant no Reefy account access.

See [workspace import](docs/workspace-import.md) before importing. Workspace admin access and plugin ownership must be verified first. The catalog intentionally omits `pluginId` until that check, so it does not silently adopt a personal plugin. Do not import it as a replacement without deciding ownership and avoiding duplicate installations.
