# Reefy Dev workspace import

This catalog requires a ChatGPT workspace with an admin and GitHub marketplace import. A personal cloud plugin is not automatically a workspace plugin, and publishing this repository alone does not activate sync.

Before import, open the existing Reefy Dev plugin under that workspace's Admin > Plugins and verify ownership and its exact ID. If it belongs to the same workspace, put that verified `pluginId` beside the catalog entry's name/source to preserve its identity and policies. A plugin from a personal account or another workspace cannot be adopted this way. Decide the migration explicitly; do not silently create a second plugin.

After those checks, import this repository under Admin > Plugins > Add > Import marketplace. Use https://github.com/reefyai/reefy-plugins as Source, leave Path empty, and choose main for future updates. Authorize only the required GitHub access. Review import results, required app availability and role policies. This repo contains no production catalog entry.

The package uses its existing registered app reference rather than direct MCP declarations, which workspace import marks desktop-only. Import does not create an app, connect accounts or grant more service permissions. Verify the registered app is available in the intended workspace.

New marketplaces sync daily. Admin > Plugins > Marketplaces > selected marketplace > Sync now requests an immediate update. After adopting an existing workspace plugin, GitHub becomes its update source and ZIP replacement is disabled.

Run package tests, regenerate the bundle and review changes before merging. Automatic sync can import future catalog entries. A successful repo build is not proof of successful workspace import or real ChatGPT acceptance.

References: https://learn.chatgpt.com/docs/enterprise/plugin-management
