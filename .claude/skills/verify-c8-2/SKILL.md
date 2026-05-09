---
name: verify-c8-2
description: Verify readiness criterion C8.2 (Observability) in the current project. Reports fulfillment level 0–3.
allowed-tools: Bash Read
---

# Verify C8.2 — Observability

## Criterion Definition

| Level | Description |
|-------|-------------|
| 0 | No access to logs or metrics |
| 1 | Read-only access to logs/metrics |
| 2 | Queryable monitoring and logs |
| 3 | Automated anomaly detection and alerting |

## Evidence

### Logging libraries in use
!`cat package.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); deps={**d.get('dependencies',{}),**d.get('devDependencies',{})}; logs=[k for k in deps if any(x in k for x in ['pino','winston','bunyan','morgan','log4','loglevel'])]; print('Logging deps:', logs if logs else 'none')" 2>/dev/null || true`
!`grep -r -i "import logging\|import structlog\|loguru\|python-json-logger" --include="*.py" -l . 2>/dev/null | head -5 || echo "(no Python logging imports found)"`

### Monitoring tool configuration
!`ls datadog.yaml .datadog/ newrelic.js newrelic.yml .newrelic/ 2>/dev/null || echo "(no Datadog/New Relic config)"`
!`ls prometheus.yml prometheus.yaml 2>/dev/null || echo "(no Prometheus config)"`
!`ls -d grafana/ 2>/dev/null || echo "(no Grafana directory)"`
!`find . -maxdepth 4 \( -name "otel*.yml" -o -name "otel*.yaml" -o -name "opentelemetry*.yml" \) 2>/dev/null | head -5 || echo "(no OpenTelemetry config files)"`

### Monitoring / observability deps
!`cat package.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); deps={**d.get('dependencies',{}),**d.get('devDependencies',{})}; obs=[k for k in deps if any(x in k for x in ['datadog','opentelemetry','@opentelemetry','prometheus','grafana','sentry','newrelic','dd-trace','elastic-apm'])]; print('Observability deps:', obs if obs else 'none')" 2>/dev/null || true`
!`grep -r -i "opentelemetry\|@opentelemetry\|dd-trace\|newrelic\|elastic-apm\|sentry" --include="*.py" --include="*.ts" --include="*.js" -l . 2>/dev/null | head -10 || echo "(no observability SDK imports)"`

### MCP / agent access to logs and metrics
!`cat .claude/settings.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); mcp=d.get('mcpServers',{}); obs=[k for k in mcp if any(x in k.lower() for x in ['grafana','datadog','cloudwatch','sentry','log','metric','monitor'])]; print('Observability MCP servers:', obs if obs else 'none')" 2>/dev/null || echo "(no observability MCP servers in settings)"`

### Alerting configuration
!`find . -maxdepth 4 \( -iname "alert*.yml" -o -iname "*.alert.yml" -o -iname "alertmanager*" -o -iname "*.rules.yml" \) 2>/dev/null | head -10 || echo "(no alerting config files)"`
!`find .github/workflows/ -name "*.yml" 2>/dev/null | xargs grep -l -i "alert\|pagerduty\|opsgenie\|incident" 2>/dev/null | head -5 || echo "(no alerting steps in CI)"`

### Sentry or error-tracking config
!`ls sentry.client.config.ts sentry.server.config.ts sentry.config.ts sentry.properties 2>/dev/null || echo "(no Sentry config files)"`

## Instructions

Analyse the evidence above and determine the fulfillment level for C8.2.

Scoring guide:
- **Level 0**: No logging libraries, no monitoring tool configuration, no observability dependencies. An agent has no way to access logs or metrics — they exist only in someone's head or in a cloud dashboard with no programmatic access.
- **Level 1**: Logging is configured (a structured logging library, cloud-native logging) and read-only access to logs/metrics is possible — e.g., an agent could call the cloud provider's API to retrieve log entries. The key is that logs exist somewhere and are readable, even if not easily queryable.
- **Level 2**: Queryable monitoring and logs — an agent can run structured queries against logs (e.g., CloudWatch Insights, Grafana Loki queries, Datadog log queries, OpenTelemetry-backed traces) or query metrics via an API. An observability MCP server that exposes query operations qualifies.
- **Level 3**: Automated anomaly detection and alerting is configured — alert rules in Grafana/Prometheus, PagerDuty/OpsGenie integration, or error-tracking thresholds (Sentry alert rules) that fire automatically without human inspection. The system proactively signals problems rather than requiring an agent to poll.

Report in exactly this format:

**C8.2 — Observability**
- **Level**: [0 / 1 / 2 / 3]
- **Rationale**: [one or two sentences citing the specific evidence]
