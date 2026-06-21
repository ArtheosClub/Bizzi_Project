# MCP_PERMISSION_MATRIX.md

# Art of Business

## MCP Permission Matrix v1.0

**Status:** Canonical Permission Matrix  
**Owner:** AG016_Compliance_Manager  
**Architecture Owner:** AG054_Enterprise_Architect  
**Operational Owner:** AG052_AI_Automation_Manager  
**Audit Owner:** AG003_AI_Auditor

---

# 1. Purpose

The MCP Permission Matrix defines which agents may access which MCP servers, tools, resources, and actions inside the Art of Business ecosystem.

It operationalizes:

- MCP Security Model;
- MCP Server Catalog;
- MCP Tool Registry;
- Agent Library authority levels;
- governance and audit rules.

---

# 2. Mission

Create a clear, auditable, and enforceable access-control model for agent-to-tool interactions.

```text
Agent
→ Role
→ Authority Level
→ MCP Server
→ MCP Tool
→ Permission
→ Approval Requirement
```

---

# 3. Permission Levels

```text
NO_ACCESS
READ
DRAFT
EXECUTE_WITH_APPROVAL
EXECUTE_WITHIN_DOMAIN
EXECUTE_ENTERPRISE
ADMIN
```

---

# 4. Risk-Based Approval Rules

```text
Low Risk      → READ / EXECUTE allowed by role
Medium Risk   → domain execution or optional approval
High Risk     → approval required
Critical Risk → human approval mandatory
```

---

# 5. Permission Schema

```yaml
agent_id:
agent_role:
domain:
authority_level:
mcp_server:
allowed_tools:
permission_level:
approval_required:
risk_limit:
audit_required:
notes:
```

---

# 6. Executive Agents

## AG001_CEO

Access Scope:

```text
Enterprise-wide
```

Permissions:

```text
All MCP Servers          READ
Strategic Tools          EXECUTE_ENTERPRISE
Critical Tools           EXECUTE_WITH_APPROVAL
Identity / Secrets       NO_ADMIN_ACCESS by default
```

Approval Rules:

- critical financial actions require human confirmation;
- access-control changes require audit logging;
- legal commitments require Legal review.

---

## AG002_Chief_Orchestrator

Access Scope:

```text
Enterprise-wide orchestration
```

Permissions:

```text
MCP-WORKFLOW             EXECUTE_ENTERPRISE
MCP-KNOWLEDGE            READ
MCP-DOCUMENTS            DRAFT
MCP-CRM                  EXECUTE_WITHIN_DOMAIN
MCP-ERP                  EXECUTE_WITH_APPROVAL
MCP-FINANCE              READ / DRAFT
MCP-GITHUB               EXECUTE_WITHIN_DOMAIN
MCP-AUDIT                READ
```

Approval Rules:

- may route decisions and tasks;
- may not approve own high-risk execution;
- critical actions require domain owner approval.

---

# 7. Governance Agents

## AG003_AI_Auditor

Permissions:

```text
MCP-AUDIT                READ / EXECUTE_WITHIN_DOMAIN
MCP-KNOWLEDGE            READ
MCP-DOCUMENTS            READ
MCP-RISK                 READ
MCP-COMPLIANCE           READ
MCP-WORKFLOW             READ
```

Restrictions:

```text
No write access to audited objects by default.
```

---

## AG004_Business_Analyst

Permissions:

```text
MCP-KNOWLEDGE            READ
MCP-DOCUMENTS            DRAFT
MCP-BI                   EXECUTE_WITHIN_DOMAIN
MCP-DATA-WAREHOUSE       READ
MCP-CRM                  READ
MCP-ERP                  READ
MCP-WORKFLOW             DRAFT
```

---

## AG005_Risk_Manager

Permissions:

```text
MCP-RISK                 EXECUTE_WITHIN_DOMAIN
MCP-COMPLIANCE           READ
MCP-AUDIT                READ
MCP-KNOWLEDGE            READ
MCP-DOCUMENTS            DRAFT
MCP-BI                   READ
```

---

# 8. Finance & Legal Agents

## AG012_Finance_Manager

Permissions:

```text
MCP-FINANCE              EXECUTE_WITHIN_DOMAIN
MCP-BI                   EXECUTE_WITHIN_DOMAIN
MCP-DOCUMENTS            DRAFT
MCP-KNOWLEDGE            READ
MCP-ERP                  READ
```

Critical Restrictions:

```text
Finance.ReleasePayment   EXECUTE_WITH_APPROVAL
Finance.ApproveBudget    EXECUTE_WITH_APPROVAL
```

---

## AG013_Tax_Manager

Permissions:

```text
MCP-FINANCE              READ
MCP-TAX                  EXECUTE_WITHIN_DOMAIN
MCP-DOCUMENTS            DRAFT
MCP-KNOWLEDGE            READ
MCP-COMPLIANCE           READ
```

---

## AG014_Funding_Manager

Permissions:

```text
MCP-GRANTS               EXECUTE_WITHIN_DOMAIN
MCP-FINANCE              READ
MCP-DOCUMENTS            DRAFT
MCP-KNOWLEDGE            READ
MCP-EMAIL                DRAFT
```

---

## AG015_Legal_Manager

Permissions:

```text
MCP-LEGAL                EXECUTE_WITHIN_DOMAIN
MCP-CONTRACTS            EXECUTE_WITHIN_DOMAIN
MCP-DOCUMENTS            DRAFT
MCP-KNOWLEDGE            READ
MCP-COMPLIANCE           READ
```

Critical Restrictions:

```text
Legal.ApproveContract    EXECUTE_WITH_APPROVAL
```

---

## AG016_Compliance_Manager

Permissions:

```text
MCP-COMPLIANCE           EXECUTE_WITHIN_DOMAIN
MCP-AUDIT                READ
MCP-RISK                 READ
MCP-DOCUMENTS            DRAFT
MCP-KNOWLEDGE            READ
```

---

# 9. Revenue Agents

## AG021_Sales_Manager

Permissions:

```text
MCP-CRM                  EXECUTE_WITHIN_DOMAIN
MCP-EMAIL                DRAFT
MCP-CALENDAR             EXECUTE_WITHIN_DOMAIN
MCP-KNOWLEDGE            READ
MCP-DOCUMENTS            DRAFT
```

High-Risk Restrictions:

```text
Email.Send               EXECUTE_WITH_APPROVAL for external recipients
CRM.CloseOpportunity     EXECUTE_WITH_APPROVAL if above threshold
```

---

## AG022_Marketing_Manager

Permissions:

```text
MCP-CRM                  READ / DRAFT
MCP-EMAIL                DRAFT
MCP-DOCUMENTS            DRAFT
MCP-BI                   EXECUTE_WITHIN_DOMAIN
MCP-KNOWLEDGE            READ
```

---

## AG023_Customer_Success_Manager

Permissions:

```text
MCP-CRM                  EXECUTE_WITHIN_DOMAIN
MCP-EMAIL                DRAFT
MCP-CALENDAR             EXECUTE_WITHIN_DOMAIN
MCP-KNOWLEDGE            READ
MCP-DOCUMENTS            DRAFT
```

---

## AG024_Partnership_Manager

Permissions:

```text
MCP-CRM                  EXECUTE_WITHIN_DOMAIN
MCP-DOCUMENTS            DRAFT
MCP-EMAIL                DRAFT
MCP-CALENDAR             EXECUTE_WITHIN_DOMAIN
MCP-KNOWLEDGE            READ
```

---

# 10. Operations Agents

## AG031_Operations_Manager

Permissions:

```text
MCP-WORKFLOW             EXECUTE_WITHIN_DOMAIN
MCP-ERP                  EXECUTE_WITHIN_DOMAIN
MCP-BI                   EXECUTE_WITHIN_DOMAIN
MCP-KNOWLEDGE            READ
MCP-DOCUMENTS            DRAFT
```

---

## AG032_Procurement_Manager

Permissions:

```text
MCP-PROCUREMENT          EXECUTE_WITHIN_DOMAIN
MCP-ERP                  READ / DRAFT
MCP-DOCUMENTS            DRAFT
MCP-KNOWLEDGE            READ
MCP-EMAIL                DRAFT
```

Critical Restrictions:

```text
Procurement.ApprovePurchaseRequest  EXECUTE_WITH_APPROVAL
```

---

## AG033_Logistics_Manager

Permissions:

```text
MCP-LOGISTICS            EXECUTE_WITHIN_DOMAIN
MCP-ERP                  READ
MCP-DOCUMENTS            DRAFT
MCP-KNOWLEDGE            READ
MCP-BI                   READ
```

---

## AG034_Project_Delivery_Manager

Permissions:

```text
MCP-WORKFLOW             EXECUTE_WITHIN_DOMAIN
MCP-CALENDAR             EXECUTE_WITHIN_DOMAIN
MCP-DOCUMENTS            DRAFT
MCP-KNOWLEDGE            READ
MCP-BI                   READ
```

---

# 11. Technology Agents

## AG051_Technology_Manager

Permissions:

```text
MCP-GITHUB               EXECUTE_WITHIN_DOMAIN
MCP-CICD                 EXECUTE_WITH_APPROVAL
MCP-CLOUD                READ / DRAFT
MCP-MONITORING           EXECUTE_WITHIN_DOMAIN
MCP-DOCUMENTS            DRAFT
```

Critical Restrictions:

```text
Cloud.DeleteInfrastructure  HUMAN_APPROVAL_MANDATORY
Cloud.UpdateInfrastructure  EXECUTE_WITH_APPROVAL
```

---

## AG052_AI_Automation_Manager

Permissions:

```text
MCP-WORKFLOW             EXECUTE_ENTERPRISE
MCP-GITHUB               EXECUTE_WITHIN_DOMAIN
MCP-MONITORING           EXECUTE_WITHIN_DOMAIN
MCP-KNOWLEDGE            READ
MCP-DOCUMENTS            DRAFT
MCP-CICD                 EXECUTE_WITH_APPROVAL
```

Restrictions:

```text
No direct access to MCP-SECRETS raw values.
```

---

## AG053_Data_Manager

Permissions:

```text
MCP-DATA-WAREHOUSE       EXECUTE_WITHIN_DOMAIN
MCP-BI                   EXECUTE_WITHIN_DOMAIN
MCP-KNOWLEDGE            EXECUTE_WITHIN_DOMAIN
MCP-DOCUMENTS            DRAFT
MCP-AUDIT                READ
```

---

## AG054_Enterprise_Architect

Permissions:

```text
MCP-KNOWLEDGE            READ
MCP-DOCUMENTS            DRAFT
MCP-GITHUB               EXECUTE_WITHIN_DOMAIN
MCP-BI                   READ
MCP-MONITORING           READ
MCP-AUDIT                READ
```

Restrictions:

```text
Architecture governance access does not imply production admin access.
```

---

# 12. Infrastructure Permissions

## MCP-IDENTITY

Default:

```text
All agents: NO_ACCESS
AG016_Compliance_Manager: READ
AG052_AI_Automation_Manager: READ / DRAFT
AG054_Enterprise_Architect: READ
```

Critical actions:

```text
Identity.GrantAccess     HUMAN_APPROVAL_MANDATORY
Identity.RevokeAccess    HUMAN_APPROVAL_MANDATORY
```

---

## MCP-SECRETS

Default:

```text
All agents: NO_ACCESS to raw secrets
```

Allowed operations:

```text
Secrets.ValidateCredential   System Only
Secrets.RotateCredential     Admin + Human Approval
Secrets.CreateCredential     Admin + Human Approval
```

---

# 13. Segregation of Duties Rules

Prohibited combinations:

```text
Create Vendor + Approve Vendor
Create Invoice + Release Payment
Create Policy + Audit Policy
Grant Access + Approve Own Access
Create Contract + Final Legal Approval
Deploy Infrastructure + Approve Own Deployment
```

---

# 14. Audit Requirements

All MCP invocations must be logged.

High-risk and critical actions must additionally record:

```text
Approval Reference
Decision Reference
Business Justification
Execution Result
Rollback Plan where applicable
```

---

# 15. Review Lifecycle

```text
Define Permission
↓
Review by Compliance
↓
Approve by Architecture Owner
↓
Implement in MCP Gateway
↓
Audit Usage
↓
Review Quarterly
```

---

# 16. KPIs

- Permission Coverage Rate;
- Authorization Compliance Rate;
- Approval Compliance Rate;
- Excess Permission Findings;
- Segregation of Duties Violations;
- Audit Completeness;
- Quarterly Permission Review Completion.

---

# 17. Risks

Potential risks:

- excessive permissions;
- unauthorized tool use;
- privilege escalation;
- weak approval enforcement;
- segregation of duties failure;
- audit gaps.

Mitigations:

- least privilege;
- approval gates;
- MCP Gateway enforcement;
- quarterly access reviews;
- audit trails;
- human approval for critical actions.

---

# 18. Architectural Role

The MCP Permission Matrix is the enforcement bridge between the Agent Library and MCP Infrastructure.

It translates agent authority into practical tool access.

```text
Agent Authority
→ MCP Permission
→ Tool Access
→ Controlled Action
```
