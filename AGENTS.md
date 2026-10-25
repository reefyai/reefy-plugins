# Reefy plugins

Keep this repository limited to distributable skills, provider adapters, public documentation and synthetic package tests. Do not include hosted implementation details, deployment configuration, credentials or account-specific acceptance evidence.

Use `shared/skills` and `shared/docs` as the authoritative workflow source. Generate provider bundles from them; do not maintain edited copies of generated references or ZIPs. Dev and production share paths and behavior. Only configured origins and host-owned identities differ.

Before changing any public Reefy contract, including manifests, MCP/REST shapes, CLI or firmware fields, obtain explicit approval explaining compatibility and migration impact. Moving an already-approved contract does not authorize changing it. Preserve registered plugin identities.

Never use em-dashes. Never commit real customer/fleet data, credentials, personalized images, account IDs, serials, network addresses or raw transcripts. Synthetic identifiers only in tests and examples. Never directly access a device without explicit approval for that access.

Run package tests and build both environments before release. Codify regression coverage in the established suites. Real-host/device E2E requires disposable fixtures and verified cleanup; never claim it passed from package tests alone. Preserve provenance and checksums.

Before changing a plugin version, read [Plugin versioning](docs/releases.md#plugin-versioning). Use the approved UTC calendar-based SemVer format, preserve published history and registered identities, and keep all generated package forms in sync.
