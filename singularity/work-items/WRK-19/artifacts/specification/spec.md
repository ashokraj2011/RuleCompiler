<!-- singularity-flow:metadata
{
  "schemaVersion": 1,
  "workId": "WRK-19",
  "workType": "spec-driven-standard",
  "phase": "specification",
  "generation": 1,
  "status": "approved",
  "generatedBy": {
    "name": "Ashok Raj",
    "email": "88361104+ashokraj2011@users.noreply.github.com",
    "login": "ashokraj2011",
    "githubLookup": "resolved"
  },
  "generatedAgent": null,
  "authorship": {
    "schemaVersion": 1,
    "producer": "human",
    "channel": "manual-in-place",
    "actor": {
      "name": "Ashok Raj",
      "email": "88361104+ashokraj2011@users.noreply.github.com",
      "login": "ashokraj2011",
      "githubLookup": "resolved"
    },
    "governedAgentContext": {
      "agentId": "product-owner"
    },
    "kernelModel": {
      "invoked": false,
      "status": "exact",
      "invocationIds": []
    },
    "externalAiUse": {
      "value": "unknown",
      "status": "unavailable"
    },
    "source": {
      "kind": "in-place",
      "filename": "spec.md",
      "mediaType": "text/markdown",
      "sha256": "607b8d81e6a472c380a99d4d3c0287264aadfffdfeaa17fdc43ead031813ee50",
      "bytes": 5650
    },
    "generation": 1,
    "publishedAt": "2026-08-18T00:04:07.763Z"
  },
  "sourceCommit": "cb3347ef18b45e6263995a519aabc0df3bba1845",
  "generationCommit": "cf8b23c97c76dfc84d001d18646a036312b5ae52",
  "publicationCommit": "cf8b23c97c76dfc84d001d18646a036312b5ae52",
  "configSha256": "1935137921d0b0b1118cfe1277c1624c8c234b350586c81e5f3ac0cf0c6052f9",
  "sourceSha256": "1683ce404a8747952d645d2594a18b7fdc6a879986ebafba368acb17eab92253",
  "template": {
    "path": "singularity/templates/spec-driven/spec.md",
    "sha256": "aa4c5c86467f07303011fde5981b819f330528435b7ce141466285cf15afdd94"
  },
  "inputs": null,
  "designSources": {
    "sets": [],
    "approved": null
  },
  "remoteAgent": null,
  "clarification": null,
  "telemetry": [
    {
      "generation": 1,
      "path": "singularity/work-items/WRK-19/telemetry/specification-gen1.json",
      "sha256": "320ba813ac71f6d96f8d92c60c2d7a0660b9b7093ceb6c12c0449e03ee30febb",
      "status": "not-invoked",
      "models": [],
      "providerCost": null
    }
  ],
  "remoteOutputs": [],
  "usage": [],
  "sequenceOverrides": [],
  "approvals": [
    {
      "decision": "approved",
      "phase": "specification",
      "at": "2026-08-18T00:07:17.278Z",
      "actor": {
        "name": "Ashok Raj",
        "email": "88361104+ashokraj2011@users.noreply.github.com",
        "login": "ashokraj2011",
        "githubLookup": "resolved"
      },
      "agent": "product-owner",
      "authorityGroup": "product-approvers",
      "identityAssurance": "configured-local",
      "channel": "copilot-selection-receipt",
      "generation": 1,
      "artifactSha256": [
        {
          "path": "singularity/work-items/WRK-19/artifacts/specification/spec.md",
          "sha256": "cae86b1594ed01ff1d535cedc8a585e0b6ec3e317d1afaaca04f95d2b5198e5a"
        }
      ],
      "artifactSet": "spec-driven-specification",
      "bundleSha256": "07c43a87c0852c6890d336069d2e4d51d56692e5b9492ec5c5fcbcd6198d8b9d",
      "reviewPacketSha256": "9abcbf7d686b86fb8b4ceb24a6813eb4e5cea30ddac323ae7daf90bb8b43cbf0",
      "checklist": [
        {
          "article": "completeness",
          "decision": "satisfied"
        },
        {
          "article": "ambiguity",
          "decision": "satisfied"
        },
        {
          "article": "consistency",
          "decision": "satisfied"
        },
        {
          "article": "verifiability",
          "decision": "satisfied"
        },
        {
          "article": "boundary-conditions",
          "decision": "satisfied"
        },
        {
          "article": "non-functional",
          "decision": "satisfied"
        }
      ],
      "checklistSha256": "f52b980ffcaf26cf59e2d5c7fb15b38c1bb7fef7e37f4a81603bdfe0b55006ab",
      "actionContext": {
        "phase": "specification",
        "label": "Specification",
        "generation": 1,
        "submittedAt": "2026-08-18T00:04:58.860Z",
        "artifacts": [
          {
            "path": "singularity/work-items/WRK-19/artifacts/specification/spec.md",
            "sha256": "cae86b1594ed01ff1d535cedc8a585e0b6ec3e317d1afaaca04f95d2b5198e5a"
          }
        ],
        "reviewPacketSha256": "9abcbf7d686b86fb8b4ceb24a6813eb4e5cea30ddac323ae7daf90bb8b43cbf0",
        "submittedSourceCommit": "cf8b23c97c76dfc84d001d18646a036312b5ae52",
        "planId": "7970bf762922d0feefb46c18"
      },
      "selfApproval": true
    }
  ],
  "selfApproval": true,
  "conformanceTree": null
}
-->

# Specification — WRK-19

## Actors

- Rule compiler authors maintain the library behavior and dialect-specific output.
- Application developers provide rule JSON and call the compiler for a SQL Server target.
- Database operators run the generated SQL against a SQL Server instance.
- QA validates that generated queries are deterministic, safe, and semantically equivalent to the original rule logic.

## User scenarios

### S1 — Compile a rule into SQL Server-compliant SQL

**Priority:** P1
**Actor:** application developer
**Context:** A rule JSON is ready and the target database is Microsoft SQL Server.

- **Given** a rule JSON that resolves to DB-backed fields and valid namespace metadata
  **When** the developer invokes the SQL Server compilation path
  **Then** the library returns a T-SQL query and parameter list that filter the target table set according to the original rule logic.

- **Given** a compound rule using multiple AND/OR clauses
  **When** the rule is compiled
  **Then** the generated predicate preserves the logical grouping and evaluation order defined by the rule input.

### S2 — Fail safely when a rule cannot be represented in SQL Server

**Priority:** P2
**Actor:** rule compiler maintainer
**Context:** An unsupported datasource, missing field mapping, or invalid operator is encountered during compilation.

- **Given** an unsupported datasource or operator
  **When** the compiler attempts to generate SQL Server output
  **Then** it raises a clear validation error or handles the unsupported branch according to the documented fallback semantics instead of producing invalid SQL.

- **Given** missing namespace or table metadata
  **When** the compiler resolves a field to a target table
  **Then** it fails before execution and identifies the missing mapping to the caller.

## Failure and empty states

- **Empty:** A request with no rules or no namespace metadata produces an explicit validation error or a documented empty-result query rather than silent miscompilation.
- **Failure:** Unsupported operators, missing field mappings, or invalid rule shapes fail fast with actionable diagnostics.
- **Partial:** If any term in a rule set is invalid, the compiler must not silently emit a partially-correct query; it must reject the input or report the invalid term set clearly.

## Permissions

- The library exposes the SQL generation API only to code paths that already have access to the rule definitions and namespace metadata.
- The compiler does not bypass database permissions; it only emits SQL for execution by callers who have authorization to run it.
- A reader without access to the underlying table metadata sees only the generated SQL structure and parameter list, not privileged schema details not already provided to the caller.

## Boundary conditions

- The SQL Server compiler must support the same practical rule sizes currently supported by the Postgres and Spark paths, with a single-rule evaluation set of up to 100 predicate terms in a standard local-development run.
- Field and table names must resolve to SQL Server-safe identifiers, and literal values must remain bound parameters or explicit safe literals rather than raw string interpolation.
- Date arithmetic, comparisons, and null semantics must be deterministic and must align with the rule evaluation model used by the compiler.

## Requirements

- **REQ-001** — The library must provide a SQL Server compilation path equivalent to the current Postgres and Spark SQL outputs and return both the generated SQL text and its bound parameter values. *(S1)*
- **REQ-002** — Generated SQL Server queries must use standard T-SQL syntax and must not rely on dialect-specific behavior outside the supported subset. *(S1)*
- **REQ-003** — The compiler must preserve the logical structure of AND/OR groupings and field comparisons from the source rule JSON when generating SQL Server predicates. *(S1)*
- **REQ-004** — Unsupported datasources, operators, or missing namespace mappings must fail fast with clear diagnostics instead of emitting invalid SQL. *(S2)*
- **REQ-005** — All user-provided values used in generated predicates must be parameterized or safely escaped so the compiler does not create SQL injection opportunities. *(S1, S2)*
- **REQ-006** — The compiler must be deterministic: identical inputs produce identical SQL text and parameter ordering across repeated runs. *(S1)*

## Non-functional requirements

- **NFR-001** — Median compilation time for a 100-term rule on a standard local development machine shall be no greater than 250 ms.
- **NFR-002** — The SQL Server output must be stable across repeated invocations for the same rule and namespace configuration.
- **NFR-003** — The generated query must contain no direct interpolation of untrusted input values.
- **NFR-004** — Compile-time errors must identify the failing field, namespace, or operator in a way that supports rapid remediation.

## Constitution articles

- None. This work item does not pin a constitution at the current revision.

## Assumptions

- SQL Server follows standard T-SQL behavior for comparisons, date functions, and null semantics.
- Namespace metadata includes an authoritative mapping from rule field names to tables and primary keys.
- Rule JSON is already parsed and normalized before the SQL Server compiler receives it.

## Out of scope

- Database migration, schema creation, or execution-plan tuning for SQL Server.
- Support for proprietary SQL Server features beyond the standard T-SQL subset needed for rule compilation.
- Conversion of non-DB-backed rule sources into SQL Server queries.
