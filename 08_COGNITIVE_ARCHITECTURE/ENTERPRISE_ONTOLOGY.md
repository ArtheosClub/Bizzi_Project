# ENTERPRISE_ONTOLOGY.md

# Art of Business

## Enterprise Ontology v2.1

Technology & MCP Domain added.

Key additions:

## Technology & MCP Domain

### MCP Infrastructure
- MCP Gateway
- MCP Server
- MCP Tool
- MCP Resource
- MCP Invocation
- MCP Result
- MCP Permission
- MCP Policy
- MCP Audit Record

### Runtime Infrastructure
- Agent Runtime
- Workflow Runtime
- Execution Runtime
- Monitoring Runtime
- Deployment Runtime

### Technology Assets
- Repository
- Source Code
- Branch
- Pull Request
- Issue
- Release
- Deployment
- Environment

### Infrastructure Assets
- Cloud Resource
- Server
- Container
- Network
- Database
- Storage
- Secret
- Credential

### Observability Assets
- Log
- Metric
- Event
- Alert
- Incident
- Audit Trail

## Additional Relationships
- Agent INVOKES MCP Tool
- MCP Tool BELONGS_TO MCP Server
- MCP Server EXPOSES MCP Resource
- MCP Invocation EXECUTED_BY Agent
- MCP Invocation USED MCP Tool
- MCP Invocation PRODUCED MCP Result
- MCP Result UPDATES Enterprise Object
- MCP Permission AUTHORIZES MCP Tool
- MCP Policy GOVERNS MCP Server
- Repository CONTAINS Source Code
- Deployment DEPLOYS Runtime
- Runtime EXECUTES Agent
- Log RECORDS MCP Invocation
- Audit Trail TRACES Decision

## Ontology IDs
- ONT-7000 Technology & MCP Domain
- ONT-7100 MCP Infrastructure
- ONT-7200 Runtime Infrastructure
- ONT-7300 Technology Assets
- ONT-7400 Infrastructure Assets
- ONT-7500 Observability Assets

This version aligns Enterprise Ontology with the complete 09_MCP_INFRASTRUCTURE architecture.