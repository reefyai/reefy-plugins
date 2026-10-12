# Reefy plugin scaffold

This development package points at the canonical `https://reefy.dev/mcp`. It does not register or publish a ChatGPT connection by itself. Register the backend connection first, validate its exact callback, then use the host's package/workspace publishing flow. The public OAuth client identifier is not a secret; no credentials belong in this package.

The package follows the [portable Agent Plugins format](https://developers.openai.com/plugins/build/plugins). Client registration and linking must be tested against the installed host before distributing it. This is a scaffold, not a verified marketplace artifact.

Production packaging changes deployment identity and domain configuration only. Use the same implementation, tool schemas, paths, and consent flow; do not fork the development backend or introduce a dev endpoint.
