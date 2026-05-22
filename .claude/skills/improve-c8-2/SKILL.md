---
name: improve-c8-2
description: Improve readiness criterion C8.2 (Observability) in the current project by adding structured logging and monitoring configuration. Raises the fulfillment level by one step.
allowed-tools: Bash Read Write Edit
---
<!--
Copyright (c) 2026 Codomain D.O.O. All rights reserved.
Licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
See LICENSE.md for details.
Licensed clients may use and modify this material for internal business purposes.
-->

# Improve C8.2 — Observability

## Current State

### Existing observability
!`cat package.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); deps={**d.get('dependencies',{}),**d.get('devDependencies',{})}; obs=[k for k in deps if any(x in k for x in ['pino','winston','bunyan','morgan','@opentelemetry','datadog','sentry','newrelic','dd-trace'])]; print('Observability deps:', obs)" 2>/dev/null || true`
!`grep -r "import logging\|import structlog\|loguru\|python-json-logger" --include="*.py" -l . 2>/dev/null | head -5 || echo "(no Python logging imports)"`
!`ls datadog.yaml prometheus.yml grafana/ 2>/dev/null || echo "(no monitoring configs)"`
!`ls sentry.client.config.ts sentry.server.config.ts sentry.config.ts 2>/dev/null || echo "(no Sentry config)"`
!`find . -maxdepth 4 -name "otel*.yml" -o -name "opentelemetry*.yml" 2>/dev/null | head -5 || echo "(no OpenTelemetry config)"`

### MCP observability access
!`cat .claude/settings.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); mcp=d.get('mcpServers',{}); obs=[k for k in mcp if any(x in k.lower() for x in ['grafana','datadog','sentry','monitor','metric','cloudwatch'])]; print('Observability MCP:', obs if obs else 'none')" 2>/dev/null || echo "(no observability MCP)"`

### Alerting
!`find . -maxdepth 4 \( -iname "alert*.yml" -o -iname "*.rules.yml" \) 2>/dev/null | head -5 || echo "(no alerting config)"`

### Language / framework
!`ls package.json 2>/dev/null && echo "Node" || true`
!`ls pyproject.toml requirements.txt 2>/dev/null && echo "Python" || true`
!`head -20 src/index.ts src/index.js src/app.ts src/app.js app/main.py main.py 2>/dev/null || echo "(no entry point found)"`

## Instructions

**Step 1 — Determine current level:**
- Level 0: No logging libraries, no monitoring configuration
- Level 1: Logging configured and read-only access to logs/metrics is possible
- Level 2: Queryable monitoring and logs (structured query API or observability MCP server)
- Level 3: Automated anomaly detection and alerting configured

**Step 2 — Implement the improvement:**

**If current level is 0 → raise to 1:**
Add structured logging appropriate to the detected language:

- **Node.js/TypeScript**: 
  1. Add `pino` and `pino-pretty` to dependencies
  2. Create `src/logger.ts` (or similar) that exports a configured pino instance with JSON output
  3. Update the main entry point to import and use the logger instead of `console.log`
  4. Add `LOG_LEVEL=info` to `.env.example`

- **Python**:
  1. Add `structlog` or `python-json-logger` to requirements
  2. Create a `logging_config.py` or add logging setup to the main module
  3. Configure JSON output format for production, human-readable for development
  4. Add `LOG_LEVEL=INFO` to `.env.example`

- **Any project**: Also add Sentry for error tracking (widely supported, free tier available):
  1. Add `@sentry/node` (Node) or `sentry-sdk` (Python) to dependencies
  2. Create a minimal Sentry initialization file that reads `SENTRY_DSN` from environment
  3. Add `SENTRY_DSN=` to `.env.example` with a comment explaining where to get it

**If current level is 1 → raise to 2:**
Level 2 requires structured query access to logs/metrics — this typically requires external infrastructure (Grafana, Datadog, CloudWatch) that cannot be fully provisioned automatically.

What can be automated:
1. Add OpenTelemetry instrumentation to make logs/traces queryable by any OTel-compatible backend:
   - Node.js: add `@opentelemetry/sdk-node`, `@opentelemetry/auto-instrumentations-node`
   - Create `src/instrumentation.ts` that initialises the OTel SDK
   - Add `OTEL_EXPORTER_OTLP_ENDPOINT=` to `.env.example`

2. Document in CLAUDE.md how to query logs:
   ```markdown
   ## Observability
   - Logs: structured JSON via pino/structlog, exportable to any OTel backend
   - To query logs locally: `docker logs <container> | jq 'select(.level == "error")'`
   - Production: configure OTEL_EXPORTER_OTLP_ENDPOINT to point to your observability backend
   ```

**If current level is 2 → raise to 3:**
Level 3 requires automated alerting infrastructure (Prometheus alert rules, PagerDuty, Sentry alert rules). This requires external service accounts and cannot be fully automated.

What can be automated:
1. If Sentry is already configured, add Sentry alert rules documentation and create a `sentry.properties` config file with alert thresholds
2. If Prometheus is in use, create an `alerts.yml` with standard alert rules (high error rate, high latency, service down)
3. Add documentation in CLAUDE.md explaining the alerting setup and how an agent can check alert status

**If already at level 3:**
Report that C8.2 is already at its maximum level (3) and no improvement is needed.

**Step 3 — Report:**
State what files were created or modified, the before and after level, and any external setup required.
