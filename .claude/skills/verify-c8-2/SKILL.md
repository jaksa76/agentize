---
name: verify-c8-2
description: Verify readiness criterion C8.2 (Observability) in the current project. Reports fulfillment level 0–3.
allowed-tools: Bash Read
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Verify C8.2 — Observability

## Criterion Definition

| Level | Description |
|-------|-------------|
| 0 | No access to logs or metrics |
| 1 | Read-only access to logs/metrics |
| 2 | Queryable monitoring and logs |
| 3 | Automated anomaly detection and alerting |

## Evidence to Gather

- Check dependency manifests for logging libraries appropriate to the project's language and for observability/monitoring SDKs.
- Look for monitoring or observability configuration files (Datadog, Prometheus, Grafana, OpenTelemetry, Sentry, etc.) anywhere in the project.
- Check the MCP server configuration for any observability servers that would allow agents to query logs or metrics.
- Look for alerting configuration files or CI steps that configure automated alerts (Prometheus alert rules, PagerDuty/OpsGenie integration, etc.).
- Look for error-tracking configuration files.

## Instructions

Gather the evidence described above and determine the fulfillment level for C8.2.

Scoring guide:
- **Level 0**: No logging libraries, no monitoring tool configuration, no observability dependencies. An agent has no way to access logs or metrics — they exist only in someone's head or in a cloud dashboard with no programmatic access.
- **Level 1**: Logging is configured (a structured logging library, cloud-native logging) and read-only access to logs/metrics is possible — e.g., an agent could call the cloud provider's API to retrieve log entries. The key is that logs exist somewhere and are readable, even if not easily queryable.
- **Level 2**: Queryable monitoring and logs — an agent can run structured queries against logs (e.g., CloudWatch Insights, Grafana Loki queries, Datadog log queries, OpenTelemetry-backed traces) or query metrics via an API. An observability MCP server that exposes query operations qualifies.
- **Level 3**: Automated anomaly detection and alerting is configured — alert rules in Grafana/Prometheus, PagerDuty/OpsGenie integration, or error-tracking thresholds (Sentry alert rules) that fire automatically without human inspection. The system proactively signals problems rather than requiring an agent to poll.

Report in exactly this format:

**C8.2 — Observability**
- **Level**: [0 / 1 / 2 / 3]
- **Rationale**: [one or two sentences citing the specific evidence]
