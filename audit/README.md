# Project Audit — `easyscience/templates`

**Date:** 2026-07-06
**Branch:** `audit`
**Scope:** The full Copier template repository — `copier.yml`, the `template/` payload
(all Jinja files, templated filenames, workflows, docs, tooling), the repo's own
build/CI config, and the generated output for `lib` / `app` / `home` / `both`.

This audit was produced by static review of every file in scope plus **live
`copier copy` renders** of four type combinations (`lib`-only, `app`-only,
`home`+`both`, `both`+`app`) to confirm actual generated output.

## Deliverables

| File | Contents |
| --- | --- |
| [`findings.md`](findings.md) | All issues, sorted by priority: **Highest → High → Medium → Low → Lowest**. Each has location, impact, and a concrete fix. |
| [`recommendations.md`](recommendations.md) | Improvement recommendations (process, structure, hardening) beyond individual bug fixes. |

## Executive summary

The **`lib` path — the template's own primary use — is solid and well-engineered.**
Config files are thoughtfully commented, CI uses least-privilege permissions and a
scoped GitHub App token, and the `_exclude_` templating mechanism is correct. The
problems cluster in four areas:

1. **The `app` and `home` template paths ship silently-broken output.** Because
   Copier's default undefined handling turns unknown variables into empty strings
   (no crash), bugs render quietly: the `home` default produces a *fully broken*
   project, and `app` projects get the wrong Python versions and cross-links to the
   wrong repositories.
2. **Broken/missing references.** Several `pixi` tasks point at scripts that don't
   exist; a tool imports an undeclared dependency (`pooch`); the app template
   references `main.py`/`main.qml` entrypoints it never ships.
3. **Supply-chain & reproducibility hardening.** Every third-party GitHub Action is
   pinned to a mutable tag/branch (not a SHA) — including the PyPI-publish action in
   an OIDC-privileged job — and this pattern propagates to every org repo. The
   committed `pixi.lock` is ~2 months stale and CI installs it `frozen`, so a
   committed fix is silently not applied.
4. **Self-validation gap.** The repo has **no tests** and no rendering checks, so all
   of the above shipped without CI noticing. An empty `src/easytemplates/` package
   and empty `tests/` tree mean the repo's own `test`/`build` tasks fail.

### Issue counts by priority

| Priority | Count |
| --- | --- |
| 🔴 Highest | 2 |
| 🟠 High | 6 |
| 🟡 Medium | 12 |
| 🔵 Low | 10 |
| ⚪ Lowest | 5 |
| **Total** | **35** |

### The five to fix first

1. `home` template default generates a broken project — **F1**.
2. `app` projects declare the wrong Python versions — **F2**.
3. Broken `pixi` task → script references (root + shipped to every repo) — **F5**.
4. `app`/`CONTRIBUTING` cross-links point at the wrong repositories — **F6**.
5. Stale `pixi.lock` + `frozen` CI hides a committed dependency fix — **F7**.

The highest-leverage *systemic* fix is **adding a render-and-check CI matrix**
(see `recommendations.md` R1) — it would have caught F1, F2, F4, F5, and F8 before release.
