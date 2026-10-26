# Pilot project format

Use a root Dockerfile and reefy/app.json. The app must serve HTTP on the declared port, run as uid 65534, and store all persistent state under /data. The builder smoke test checks the root HTTP endpoint. Use dependencies appropriate to the user's app and build/test locally before publication.

Minimal supported manifest:

```json
{
  "slug": "reef-notes",
  "name": "Reef Notes",
  "description": "Private notes on your Reefy device",
  "version": "1.0.0",
  "image": "reefy-local/reef-notes:1.0.0",
  "default_port": 8080,
  "needs_llm": false,
  "volumes": {"data": {"mount": "/data", "uid": 65534, "backup": ["borgbase"]}}
}
```

The builder supplies the built immutable image reference. Keep Dockerfile USER 65534 and bind the default bridge-network server to 0.0.0.0. Do not request host sockets, privileged containers, host paths, extra capabilities or device credentials. Change version for every publication and retain the same data mount for updates. This pilot supports the single-container format above; do not silently assume arbitrary compose, GPU or LLM wiring is available.


## LAN discovery

Bridge networking remains the default. When the requested app needs device-LAN
multicast discovery, opt into existing `network_mode: "host"` and
`dynamic_port: true` fields in reefy/app.json. This shares the device network
namespace without granting extra capabilities or host paths. Explain this
network access when updating the app, and retain the existing project, app
instance and data volume. Publish a new version, then update that instance.

For default_port 8080, read APP_PORT_8080 and bind the HTTP listener to
127.0.0.1 at that allocated port when present. Without the variable, listen on
0.0.0.0:8080 for the isolated build health check. Keep multicast discovery
separate from HTTP binding. Build/check containers never use host networking.
Continue using Reefy's authenticated Open app link; do not expose the UI
directly on all host interfaces or request direct_lan routing.
