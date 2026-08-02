# Epoch IV — Engineering Governance

Document ID: EPOCH-IV-ENGINEERING-GOVERNANCE
Title: Epoch IV Engineering Governance
Version: 1.0
Status: ACTIVE
Document Type: Engineering Governance — Rules of Conduct
Part of: Epoch IV Engineering Governance Package
Authority: Project Owner, per the Authority Hierarchy confirmed in
`40_GATE_C/GC-005_GATE_C_CLOSURE_DECISION.md` §1
Repository: ArtheosClub/Bizzi_Project

This document SHALL define the engineering rules governing implementation
conduct under Epoch IV. This document SHALL NOT modify DECISION_0003,
the Architecture Baseline, the Engineering Baseline, or any Gate C
Certification document. Where this document conflicts with the
Architecture Baseline, the Engineering Baseline, the Implementation
Baseline, or any Gate C Certification document, the higher-authority
document prevails.

---

## 1. Repository Rules

Every implementation artifact SHALL reside in its governance-designated
location within the repository. No implementation artifact SHALL be
committed outside the repository structure established for it. Every
repository artifact SHALL remain traceable to its authoritative source.

---

## 2. Branching Strategy

`main` SHALL remain the Official Implementation Branch, per DECISION_0003
§9. No direct commit SHALL be made to `main`. All implementation work
SHALL originate from a short-lived feature branch. Architecture work
SHALL originate from a dedicated architecture branch, kept separate from
implementation feature branches, per DECISION_0003 §9.

---

## 3. Pull Request Requirements

Every implementation pull request SHALL reference its applicable Work
Package, its applicable ADR(s), the Engineering Baseline, and
DECISION_0003, per DECISION_0003 §10. Every Pull Request SHALL pass
automated validation before merge. No Pull Request SHALL be merged while
a condition requiring governance escalation, per §18 below, is active.

---

## 4. Code Review Policy

Every implementation change SHALL undergo review before merge. Review
SHALL verify conformance to the Architecture Baseline, conformance to
applicable ADRs, and conformance to this document. No implementation
change SHALL be self-merged without review, except where governance
procedure elsewhere in the repository explicitly permits it.

---

## 5. Definition of Done

Every module SHALL satisfy the following before merge: conformance to
its module specification; satisfaction of its defined verification
criteria, per `IMPLEMENTATION_STRATEGY.md` §2.4; conformance to the
Architecture Baseline and to every applicable ADR; satisfaction of the
Testing Requirements (§6) and Documentation Requirements (§7) below. A
module failing any of the foregoing SHALL NOT be considered done.

---

## 6. Testing Requirements

Every implementation unit SHALL be accompanied by verification
sufficient to demonstrate satisfaction of its defined verification
criteria. No implementation unit SHALL be merged absent such
verification. No test SHALL be skipped to force implementation progress.

---

## 7. Documentation Requirements

Every module SHALL be accompanied by documentation sufficient to
describe its interface, its conformance to the Architecture Baseline,
and its relationship to applicable ADRs. Documentation SHALL be updated
concurrently with the implementation it describes, not deferred to a
later cycle.

---

## 8. Architecture Compliance

No implementation SHALL modify the Architecture Baseline without
Governance approval. Every architectural deviation SHALL require ADR
approval before merge, per §9 below. Every implementation SHALL
reference an approved specification.

---

## 9. ADR Compliance

Every architectural deviation SHALL require ADR approval. No
implementation unit SHALL proceed in contradiction of a currently
approved Architecture Decision Record. A proposed deviation from an
approved ADR SHALL be recorded as a new or superseding ADR before the
deviating implementation is merged.

---

## 10. Coding Standards

Every implementation unit SHALL conform to the coding standards
established under the project's engineering governance framework. A
deviation from an established coding standard SHALL be recorded and
justified. No implementation unit inconsistent with an established
coding standard SHALL be considered done, per §5 above.

---

## 11. Dependency Management

Every dependency introduced by implementation SHALL be recorded and
justified against the approved Technology Stack, consistent with the
Engineering Baseline. No dependency SHALL be introduced that contradicts
an approved ADR. Every dependency SHALL be reviewed for currency and
known vulnerability before introduction.

---

## 12. Versioning

Every versioned implementation artifact SHALL declare an explicit
version. Every version increment SHALL be traceable to the change that
produced it. No versioned artifact SHALL be modified without a
corresponding version change, where the artifact's own governance
convention requires one.

---

## 13. Security Requirements

Every implementation unit SHALL assume the more restrictive security
posture wherever authority is undetermined. No raw secret, token, or
password SHALL appear in a log, event, or response. No query or response
SHALL cross a workspace boundary. No authorization bypass SHALL be
introduced.

---

## 14. Logging

Every state-changing implementation action SHALL produce a corresponding
audit event. No log SHALL contain a raw secret, token, or password.

---

## 15. Observability

Every implementation unit SHALL be implemented such that its operational
state is observable, consistent with the Engineering Baseline. No
implementation unit SHALL be considered done absent the observability
its Definition of Done (§5) requires.

---

## 16. CI Requirements

Every implementation change SHALL be validated by Continuous Integration
before merge. CI SHALL NOT be repeatedly failing at merge time. No
implementation change SHALL bypass CI validation.

---

## 17. Release Rules

Every release SHALL originate from the Official Implementation Branch
(`main`), per DECISION_0003 §9. No release SHALL include an
implementation unit that has not satisfied its Definition of Done (§5).
Every release SHALL preserve traceability to the Work Packages, ADRs,
and governance instruments it implements.

---

## 18. Governance Escalation

Where a condition arises that engineering authority is not empowered to
resolve — including any architectural deviation, any authorization
ambiguity, or any conflict between this document and a higher-authority
governance instrument — implementation SHALL halt on that matter, and
the matter SHALL be escalated to the Project Owner. No engineering
authority SHALL resolve a matter reserved to architectural or
governance authority.
