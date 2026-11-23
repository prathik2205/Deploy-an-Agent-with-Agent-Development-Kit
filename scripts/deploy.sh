#!/usr/bin/env bash
set -euo pipefail
cp .env paint_agent/.env
adk deploy agent_engine --display_name "Paint Agent" paint_agent
# Copy the printed resource name into .env as AGENT_RESOURCE_NAME
