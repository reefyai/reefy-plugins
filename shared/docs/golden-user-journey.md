# Reefy apps golden user journey

## Main tenets

The user states their setup goal once. Keep choices and progress across account linking, hardware preparation and pending operations. Minimize questions and routine web visits, arrange supported event continuation automatically, and verify the final outcome. Use one shared journey across apps and assistant providers, with explicit host capability differences.

Dev and production use the same code, endpoint paths and contracts. The connected deployment determines all Reefy links, credentials and account data. Both use `/mcp`. Do not introduce dev-only paths or switch environments during setup.

## Journey

1. Identify the requested app and known account/device context. Returning users can reuse an adopted device. Authentication failure must not be interpreted as an empty account.
2. If hardware is needed, guide a tested computer-plus-USB selection or compatible existing hardware. Follow [device onboarding](device-onboarding.md) for account-bound image download, Etcher flashing and USB boot. Ask before any purchase or destructive write.
3. Connect the Reefy account through the host's supported OAuth flow. Reefy's Google/GitHub sign-in identifies the user; Reefy's separate OAuth grant authorizes the assistant. Resume the existing goal after returning. Never ask for credentials in chat.
4. Identify the intended account-owned new device. Recommend eligible internal storage for a dedicated PC, show its reported model/capacity and exact target, and ask before erasing it. Preserve storage if consent is declined. Use the existing web UI storage behavior; no new firmware capability is required by MCP.
5. Adopt once, save the operation ID and arrange temporary, scoped event continuation where supported. Re-read authoritative state after subscription to catch races. Backend acceptance is not device readiness. Stop monitoring after completion, failure or cancellation.
6. Install the selected supported app once, track readiness through the same operation/event lifecycle and continue already-authorized configuration. Do not duplicate instances on retries or infer new permissions from events.
7. Complete app-specific setup through secure provider authorization/pairing when required. Chaos Coordinator is the first reference app, not a required dependency for all apps. Its provider and WhatsApp steps illustrate additional app-specific handoffs.
8. Verify an app-specific usable outcome. For a web app, resolve its authorized instance launch control and show one Open app action when ready. Background completion replies include one explicit owner app link in the reply itself, since a host may omit task-generated UI cards. Voice gives a short cue instead of reading the URL aloud. Route readiness and running-container status are separate. Do not create a share link merely to open the owner's app.
9. Later requests can check devices, describe cached hardware or start another supported app. Keep the web dashboard available for advanced configuration and recovery.

## Host constraints and acceptance

MCP connectivity alone does not guarantee background execution. Only claim monitoring after a supported event subscription succeeds. On an unsupported host, preserve progress and provide one minimal resume action. Do not promise system-browser selection unless that client has been verified.

Account ownership, explicit erasure consent, scoped credentials, idempotent operations and backend checks are required throughout. Skills guide behavior; backend authorization remains authoritative. Never infer missing hardware details or readiness.

This is the shared product target. Tool availability, app-specific configuration and provider distribution must be validated against the deployed implementation. No new public contracts are defined here. Real-host E2E must cover successful and failed operations, consent, environment/account isolation, duplicate events, interrupted handoffs, app launch and verified fixture cleanup.

## Firmware maintenance during setup

Check firmware independently from internal-storage selection. Offer a short reboot/interruption approval when an update is available, and explain accurately when the general adoption rule requires it. Use the connected account's supported update tool, retain the requested name and app, and resume after fresh device-reported version verification. An unadopted reboot starts normal rediscovery with the saved request context and a new adoption operation; do not extend subscriptions across temporary UUIDs or add disk-matching steps. No user refresh request should be needed. Existing SSD erasure confirmation still applies; firmware approval does not grant it. Keep event monitoring and the firmware progress card, with honest host/Voice delivery limitations. Uncertain update outcomes never trigger automatic retries.
