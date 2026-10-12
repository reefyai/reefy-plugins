# Reefy MCP API compatibility

The existing Reefy tool contracts served at `/mcp` are Reefy API v1. This is a compatibility policy, not a new wire field or endpoint. Existing clients keep using `/mcp` without migration.

Three versions have distinct purposes:

- MCP protocol version: the transport/protocol version negotiated by the client and server.
- Reefy API compatibility generation: the published tool contracts, currently v1.
- Plugin package version: the distributed manifest, instructions and assets.

## Stable published contracts

Preserve existing tool names, accepted inputs, output fields, permission requirements and behavior for published packages. A plugin package version bump alone does not authorize a breaking MCP API change. Endpoint domains select the deployment; paths and contract behavior stay the same across dev and production.

Compatible improvements can fix implementation errors without violating documented behavior. Additive changes must remain usable by existing clients and preserve their assumptions. Do not turn an optional input into a required one, remove a result field, change its type or meaning, broaden side effects, or silently require another permission on an existing tool.

For a breaking change, introduce a separately named tool and retain the original contract while published packages depend on it. Publish and test updated guidance before moving users to the replacement. Deprecation does not immediately remove the old tool; removal requires an explicit migration plan and approval.

The existing tools are not renamed with a version suffix retroactively. No `/mcp/v1` path or additional OAuth scope is introduced by this policy. Future breaking tools need their own approved names and documented compatibility impact.

## Release checks

Keep synthetic contract tests for published tools. Before a hosted release, validate old installed package behavior as well as the current package. Include negative authorization cases and side-effect checks. Record the package revision and compatible API generation in release validation. Refresh or rescan changed definitions using the host's supported process.

Only claim real ChatGPT acceptance after testing in that host. Package validation cannot establish event continuation, account linking or device readiness. Keep account-specific results outside the distributed package.
