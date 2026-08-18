<!-- singularity-flow:metadata
{
  "schemaVersion": 1,
  "workId": "WRK-19",
  "workType": "spec-driven-standard",
  "phase": "implementation",
  "generation": 1,
  "status": "in_progress",
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
      "agentId": "architect"
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
      "filename": "implementation-summary.md",
      "mediaType": "text/markdown",
      "sha256": "43cfe4e42953c5131e09551f3a222cc5dfe98053b30792df428fe455b243a38d",
      "bytes": 31380
    },
    "generation": 1,
    "publishedAt": "2026-08-18T00:31:29.051Z"
  },
  "sourceCommit": "9261bb615b378de35403efb4eec084d50970bb65",
  "generationCommit": null,
  "publicationCommit": null,
  "configSha256": "1935137921d0b0b1118cfe1277c1624c8c234b350586c81e5f3ac0cf0c6052f9",
  "sourceSha256": "1683ce404a8747952d645d2594a18b7fdc6a879986ebafba368acb17eab92253",
  "template": {
    "path": "singularity/templates/common/implementation.md",
    "sha256": "5d0478b18c8fd14221e14c68e6238b909bccd6802a70262c416005354716c62c"
  },
  "inputs": {
    "generation": 1,
    "path": "singularity/work-items/WRK-19/context/inputs-implementation-gen1.json",
    "sha256": "e8ee6a75e167c35644ac7869c7b72a66e08ff9696d3128509e3fe0ada3de35af",
    "renderedSha256": "b95753d0be01e6f0aedd14b74027dace303039eeecf0bc677852b154fe39ebf1",
    "mode": "enforce"
  },
  "designSources": {
    "sets": [],
    "approved": null
  },
  "remoteAgent": null,
  "clarification": null,
  "telemetry": [
    {
      "generation": 1,
      "path": "singularity/work-items/WRK-19/telemetry/implementation-gen1.json",
      "sha256": "5c50ea31ee1d70ee423cac7943e58ceadda34988f651fdc3ef8ccc01498de236",
      "status": "not-invoked",
      "models": [],
      "providerCost": null
    }
  ],
  "remoteOutputs": [],
  "usage": [],
  "sequenceOverrides": [],
  "approvals": [],
  "selfApproval": false,
  "conformanceTree": null
}
-->

# WRK-19 — Implementation Summary

## Implemented outcome

Added SQL Server compilation support to the rule compiler by introducing a dedicated `SqlServerCompiler` that reuses the existing shared predicate-generation flow from `BaseSqlCompiler` while translating relative dates and literal handling into T-SQL equivalents. The public `RuleCompiler` API now exposes `to_sql_server_sql(...)` alongside the existing Postgres and Spark methods.

## Changed components and decisions

- `ccre_rulekit/compilers/sqlserver.py`: new SQL Server-specific compiler implementation with T-SQL date literals and safe literal handling.
- `ccre_rulekit/compiler.py`: exported the SQL Server compiler and added the `to_sql_server_sql` entry point.
- `tests/test_basic.py`: added focused SQL Server rule-generation tests covering single-rule compilation and relative-date rendering.
- No database migration or schema changes were required; the change is limited to compiler output generation and validation.

## Tests and operational notes

- Ran the targeted compiler tests with `pytest tests/test_basic.py`.
- Validation covers the SQL Server path and ensures it remains aligned with the current Postgres and Spark behavior for shared rule semantics.
- Known limitation: this implementation targets the standard T-SQL subset used by the compiler abstraction and does not add proprietary SQL Server-specific features beyond the standard date-add logic needed for rule evaluation.

<!-- singularity-flow:inputs:start -->

# Approved phase inputs

## Approved phase input: specification

<!-- source=artifacts/specification/spec.md sha256=e54c8a6d9c9a394473686513d50f43d8f06519bbad22ca1086a88524eb3e368e status=captured -->

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

## Approved phase input: planning

<!-- source=artifacts/planning/plan.md sha256=17d548cca4f697cef158da2ef3e4bb4590aacca708bc6fbbb8da8a084bd947ea status=captured -->

<!-- singularity-flow:metadata
{
  "schemaVersion": 1,
  "workId": "WRK-19",
  "workType": "spec-driven-standard",
  "phase": "planning",
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
      "filename": "plan.md",
      "mediaType": "text/markdown",
      "sha256": "2421f1a6fb5e7672c8e4684aa377283fba14c8ebc3b9ccf7dc3b897a6f060a9e",
      "bytes": 15030
    },
    "generation": 1,
    "publishedAt": "2026-08-18T00:10:58.189Z"
  },
  "sourceCommit": "9ae4f9010231e8d080e9b007aec26628966d6fbb",
  "generationCommit": "5105edcdd9410b2dd5d64d66f3a2062ba01e350b",
  "publicationCommit": "5105edcdd9410b2dd5d64d66f3a2062ba01e350b",
  "configSha256": "1935137921d0b0b1118cfe1277c1624c8c234b350586c81e5f3ac0cf0c6052f9",
  "sourceSha256": "1683ce404a8747952d645d2594a18b7fdc6a879986ebafba368acb17eab92253",
  "template": {
    "path": "singularity/templates/spec-driven/plan.md",
    "sha256": "303b6402e8c2c925c3507ce1eafe95bb08a69d097509cb6f8a0b5e3bee1db23f"
  },
  "inputs": {
    "generation": 1,
    "path": "singularity/work-items/WRK-19/context/inputs-planning-gen1.json",
    "sha256": "3e799a136298f4aa375c43d77177d65dca8a5fd3a9aa0d9f356a75af1a27d559",
    "renderedSha256": "00c7944fcd3d4ec0455191ef076e1a0324ea191000148e2bef6ad9e98aa11cea",
    "mode": "enforce"
  },
  "designSources": {
    "sets": [],
    "approved": null
  },
  "remoteAgent": null,
  "clarification": null,
  "telemetry": [
    {
      "generation": 1,
      "path": "singularity/work-items/WRK-19/telemetry/planning-gen1.json",
      "sha256": "168d777ab982405115599f7d3903ba143a40afddbef2ff06f81f7f3a9fc994aa",
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
      "phase": "planning",
      "at": "2026-08-18T00:13:48.316Z",
      "actor": {
        "name": "Ashok Raj",
        "email": "88361104+ashokraj2011@users.noreply.github.com",
        "login": "ashokraj2011",
        "githubLookup": "resolved"
      },
      "agent": "architect",
      "authorityGroup": "architecture-reviewers",
      "identityAssurance": "configured-local",
      "channel": "copilot-selection-receipt",
      "generation": 1,
      "artifactSha256": [
        {
          "path": "singularity/work-items/WRK-19/artifacts/planning/plan.md",
          "sha256": "03e8b1382509c5080605973dbe7120b59d1237b9ae49c3002af59ee59e483efa"
        }
      ],
      "artifactSet": "spec-driven-planning",
      "bundleSha256": "87c0cfb928c01ebe7ba2c24003fcc3bb6d91acc39221c66d2881317fc373369f",
      "reviewPacketSha256": "6271241286f9ffec74d9e4033ce1c448377b44ba6e0455b7b277df669de58a52",
      "actionContext": {
        "phase": "planning",
        "label": "Planning",
        "generation": 1,
        "submittedAt": "2026-08-18T00:12:33.964Z",
        "artifacts": [
          {
            "path": "singularity/work-items/WRK-19/artifacts/planning/plan.md",
            "sha256": "03e8b1382509c5080605973dbe7120b59d1237b9ae49c3002af59ee59e483efa"
          }
        ],
        "reviewPacketSha256": "6271241286f9ffec74d9e4033ce1c448377b44ba6e0455b7b277df669de58a52",
        "submittedSourceCommit": "5105edcdd9410b2dd5d64d66f3a2062ba01e350b",
        "planId": "88e19f7ed6fa15c9dc735b38"
      },
      "selfApproval": true
    }
  ],
  "selfApproval": true,
  "conformanceTree": null
}
-->

# Implementation plan — WRK-19

Derived from the approved specification. Cite the clause each decision serves, so convergence can
join intent to implementation at requirement altitude rather than by path `[SPK:REQ-071]`.

## Approach

Implement a dedicated SQL Server compiler that reuses the existing `BaseSqlCompiler` predicate-generation framework and only overrides the dialect-specific SQL fragments that differ from Postgres. This keeps the rule semantics consistent across dialects while isolating SQL Server syntax, parameter handling, and date expressions in one surface. The alternative—rewriting predicate logic per call site—would duplicate logic and increase the chance of behavioral drift between dialects.

## Affected surfaces

Modules, contracts, data, and interfaces this touches. Expected paths are a planning aid; the
authority on what actually changed remains reconciliation `[SPK:CON-031]`.

| Surface | Change | Serves |
|---|---|---|
| `ccre_rulekit/compilers/base_sql.py` | Confirm the generic SQL generation model remains dialect-neutral and safe for SQL Server parameter formatting, join logic, and identifier quoting. | REQ-001, REQ-003, REQ-005, REQ-006 |
| `ccre_rulekit/compilers/postgres.py` | Use as the reference implementation for SQL generation semantics and date behavior. | REQ-001, REQ-002, REQ-003 |
| `ccre_rulekit/compilers/sqlserver.py` | Add a new SQL Server compiler subclass with T-SQL-specific literal rendering and relative-date handling. | REQ-001, REQ-002, REQ-004 |
| `ccre_rulekit/compiler.py` | Expose a `to_sql_server_sql` entry point alongside the existing Postgres and Spark APIs. | REQ-001, REQ-002 |
| `tests/test_basic.py` | Add deterministic tests for single-rule compilation, unsupported operators, and date arithmetic. | REQ-001, REQ-004, REQ-006 |
| `README.md` | Document the new SQL Server target usage and limitations for developers. | REQ-001, REQ-002 |

## Sequencing

The order the work has to happen in, and what each step unblocks.

1. Audit the shared compiler contract in `BaseSqlCompiler` and map the SQL Server differences to the existing dialect abstraction.
2. Implement `ccre_rulekit/compilers/sqlserver.py` with SQL Server-specific handling for relative dates and identifier safety.
3. Expose `RuleCompiler.to_sql_server_sql(...)` in `ccre_rulekit/compiler.py` so callers use the same contract as the Postgres and Spark compilers.
4. Add focused tests covering single-rule SQL generation, unsupported datasource failure, and date comparison semantics.
5. Run the relevant pytest subset and fix any drift between SQL Server output and the existing compiler contract.

## Test strategy

How each requirement will be proved. A requirement with no stated means of proof is a requirement
that will be argued about at verification.

| Clause | Proof |
|---|---|
| REQ-001 | New SQL Server compilation tests assert the public compiler API returns both SQL text and bound parameters for valid rules. |
| REQ-002 | Validate generated queries use T-SQL-safe identifiers and no unsupported Postgres-only syntax is emitted. |
| REQ-003 | Compare the rule JSON grouping and `AND`/`OR` expression structure against the output predicate tree for a multi-term rule. |
| REQ-004 | Add unsupported datasource/operator tests asserting the compiler fails early with actionable diagnostics instead of invalid SQL. |
| REQ-005 | Verify parameterized values are used for user-supplied literal inputs and no direct interpolation occurs within the SQL string. |
| REQ-006 | Re-run the same SQL Server compilation input and assert identical SQL text and parameter ordering across repeated invocations. |
| NFR-001 | Use a lightweight local benchmark or test hook to confirm compilation remains fast enough for a 100-term rule in development. |
| NFR-004 | Check diagnostics include the failing field/namespace/operator in failing test assertions. |

## Constitution articles

None. This work item does not pin a constitution at the current revision.

## Risks and rollback

The main risk is dialect drift: SQL Server date functions and identifier quoting differ from Postgres and Spark. This will be noticed through golden SQL tests and by failing unsupported-input assertions. The rollback path is simple: keep the new compiler isolated in a dedicated module and expose it through a single API entry point, so removing the new dialect support does not require changing the generic compiler contract or other dialect implementations.

<!-- approved source inputs:start -->

# Approved phase inputs

## Approved phase input: specification

<!-- source=artifacts/specification/spec.md sha256=e54c8a6d9c9a394473686513d50f43d8f06519bbad22ca1086a88524eb3e368e status=captured -->

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

<!-- approved source inputs:end -->

<!-- singularity-flow:inputs:end -->
