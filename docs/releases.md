# Package releases and review

1. Make the workflow change in the shared source, with synthetic package regression coverage.
2. Run package tests and build both environments from the same commit. Check bundled references, URLs, identity and ZIP contents.
3. Run MCP compatibility and real-host acceptance checks against the intended deployment. Use disposable devices and verified cleanup. Package unit tests are not real ChatGPT E2E evidence.
4. Update the changelog. Record package version, repository commit, checksums and compatible backend revision. Tag a validated source revision when preparing a release; CI retains its package artifacts.
5. For an existing private connection, use the registered-package helper with the privately downloaded ZIP and verify the installed identity, version, skill and reference. Do not replace its mapping with a scaffold.
6. For public submission, build the portable MCP package and complete publisher/listing requirements and review. Current OpenAI public submission rejects `.app.json` references. Keep reviewer credentials and instructions in the secure portal, outside this repository and ZIP.
7. Deploy backward-compatible backend changes independently. Rescan/refresh tool definitions through the supported host workflow when needed. Package instruction/metadata updates use the package distribution process.

Do not edit generated ZIPs as the source of truth. Preserve installed connection identities. Public GitHub commits and tags alone do not update a ChatGPT public directory release.

Reviewer account: dedicated sample tenant, ready-to-use synthetic devices/apps and no interactive MFA/email/SMS prerequisite. Test all submitted scenarios before review. Keep real accounts, access credentials, fleet identifiers and account-specific acceptance evidence outside this repository.

References:

- https://developers.openai.com/plugins/build/plugins
- https://developers.openai.com/plugins/deploy/submission
- https://developers.openai.com/plugins/deploy/app-review
