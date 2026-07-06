# Findings — `easyscience/templates`

Issues sorted by priority: **Highest → High → Medium → Low → Lowest**.
Every claim was verified against actual file contents; templating issues were
confirmed with live `copier copy` renders. Locations use `path:line`.

> **Key context:** Copier's default Jinja does **not** use `StrictUndefined`, so an
> undefined/unset variable renders as an **empty string** instead of crashing. This
> is why several serious bugs below are *silent* — the render "succeeds" but the
> output is wrong.

## Summary table

| ID | Priority | Category | Summary |
| --- | --- | --- | --- |
| F1 | 🔴 Highest | Templating | `template_type=home` (the default) renders a fully broken project |
| F2 | 🔴 Highest | Templating | `app` projects declare the wrong Python versions |
| F3 | 🟠 High | Security | Third-party Actions pinned to mutable tags/branches (incl. PyPI publish in OIDC job) |
| F4 | 🟠 High | Correctness | App `test.yml` references undefined `PIXI_ENVS` |
| F5 | 🟠 High | Correctness | `pixi` tasks reference tool scripts that don't exist |
| F6 | 🟠 High | Templating | `app` README & all `CONTRIBUTING` cross-link to the wrong repo |
| F7 | 🟠 High | Reproducibility | Stale `pixi.lock` + `frozen` CI hides committed dependency fix |
| F8 | 🟠 High | Quality | Repo has no tests; empty `src/easytemplates/` breaks build/test tasks |
| F9 | 🟡 Medium | Correctness | `home` ships CI workflows referencing files it never generates |
| F10 | 🟡 Medium | Dependency | `update_docs_assets.py` imports `pooch`, which isn't a dependency |
| F11 | 🟡 Medium | Completeness | `app` template is a stub: missing entrypoints, broken QML URLs |
| F12 | 🟡 Medium | Security | `pull_request_target` grants write + secrets on fork PRs (fragile) |
| F13 | 🟡 Medium | Correctness | `setup-easyscience-bot` feeds App ID into the `client-id` input |
| F14 | 🟡 Medium | Config | `lib_doi` and `app_doi` share an identical placeholder DOI |
| F15 | 🟡 Medium | CI integrity | `pydoclint` & `format-docstring` globally disabled — green check verifies nothing |
| F16 | 🟡 Medium | Templating | Template ships no `.gitattributes`; generated repos get noisy `pixi.lock` merges |
| F17 | 🟡 Medium | Tooling | All pre-commit hooks are `stages: [manual]`; `pre-commit-install` is a no-op |
| F18 | 🟡 Medium | Templating | `mkdocs.yml` uses `home_repo_name` unconditionally (broken for lib/app-only) |
| F19 | 🟡 Medium | Config | No `_min_copier_version` / `_envops`; relies on lenient-undefined to mask bugs |
| F20 | 🟡 Medium | Docs | Root `CONTRIBUTING.md` references nonexistent `pixi run spdx-add` |
| F21 | 🟡 Medium | Hygiene | Repo's own `.copier-answers.yml` `_commit` is 2 releases stale |
| F22 | 🔵 Low | Maintainability | No Dependabot/Renovate config (root or template) |
| F23 | 🔵 Low | Governance | No `SECURITY.md`, `CODEOWNERS`, or issue/PR templates shipped |
| F24 | 🔵 Low | Docs | Docs claim `pixi run check` runs unit tests; root config's hook set doesn't |
| F25 | 🔵 Low | Security | `github.head_ref` flows into unquoted shell paths (low risk) |
| F26 | 🔵 Low | Templating | `docs.yml` hardcodes `-lib` in artifact name for all types |
| F27 | 🔵 Low | Config | `.badgery.yaml.jinja` mixes `file:` and `workflow:` keys |
| F28 | 🔵 Low | Governance | `master` ruleset requires 0 approvals and no status checks |
| F29 | 🔵 Low | Docs | README duplicate section titles & broken ordered-list numbering |
| F30 | 🔵 Low | Security | `release-pr.yml` interpolates `${{ env.SOURCE_BRANCH }}` inside `run:` |
| F31 | 🔵 Low | Correctness | `pypi-test.yml` has a dead `pull_request` concurrency reference |
| F32 | ⚪ Lowest | Maintenance | Pinned Actions are 1 version behind (checkout/codecov/setup-pixi) |
| F33 | ⚪ Lowest | Maintainability | `coverage.yml` job comments mislabeled ("Job 4", no Job 3) |
| F34 | ⚪ Lowest | CI | Root runs `notebook-lint-check` but has no notebooks |
| F35 | ⚪ Lowest | Cleanliness | Dead/unused Jinja `set` vars (`current_type`, `docs_url`) in some templates |

---

## 🔴 Highest

### F1 — `template_type=home` (the default) renders a fully broken project
**Category:** Templating correctness / orphaned output
**Locations:** `copier.yml:78` (default `home`), `template/pyproject.toml.jinja:1-13,20,34,38,109`, `template/pixi.toml.jinja:1-9,78,90,186-189`, `template/src/{{lib_package_name if template_type == 'lib' else app_package_name}}/__init__.py.jinja`

`copier.yml:81` documents `home` as *"Creates shared metadata only"*, but the `home`
path renders a complete Python project. `pyproject.toml.jinja` / `pixi.toml.jinja`
only set `package_name`/`repo_name` inside the `lib` and `app` branches — there is no
`home` branch — so for `home` they are empty. Verified rendered output:

- `pyproject.toml` → `name = ''`, `packages = ['src/']`, `Documentation = ''`,
  `'Source Code' = 'https://github.com/easyscience/'`. An empty `name` is rejected by
  `validate-pyproject` and hatchling.
- `pixi.toml` → line 78 becomes ` = { path = '.', editable = true, ... }` and line 90
  ` = '*'` — an **empty TOML key**; `pixi` fails to parse the file.
- `src/<app_pkg>/__init__.py` is still created (path resolves to `app_package_name`
  since `template_type != 'lib'`) with an SPDX header but **no docstring** (neither
  branch matches for `home`).

**Impact:** The documented, **default** choice, applied via a plain
`copier copy … --data template_type=home`, yields a repo where `pixi install`,
`pyproject-check`, and any build fail immediately. It only works today because the
`README.md:178` command passes `--exclude '*' --exclude '!.gitignore' …` — i.e. the
safety lives in a CLI flag a user must remember, not in the template.

**Fix:** Add a `home` branch to the two `.jinja` headers, and exclude code/CI files
(`pyproject.toml`, `pixi.toml`, `src/**`, `tests/**`, `docs/**`, `coverage.yml`,
`dashboard.yml`, `test-trigger.yml`) for `template_type == 'home'` — via
`_exclude_`-prefixed filename conditionals or by baking the excludes into
`copier.yml`'s `_exclude`. (See also F9.)

### F2 — `app`-only `pyproject.toml` declares the wrong Python versions
**Category:** Templating correctness (`lib_` vs `app_` confusion)
**Location:** `template/pyproject.toml.jinja:34-38`

The header (`:7-12`) correctly derives `python_min`/`python_max` from `app_python` for
`template_type == "app"`, but the body ignores them and hardcodes `lib_python_*`:

```jinja
{%- for version in range(lib_python_min.split('.')[1] | int, lib_python_max.split('.')[1] | int + 1) %}  # line 34
requires-python = '>={{ lib_python_min }}'                                                                 # line 38
```

For an app-only project (`app_python=3.13`; lib questions never asked, so
`lib_python_min` falls back to its default `3.11`), the rendered `pyproject.toml` says
`requires-python = '>=3.11'` and lists classifiers `3.11`–`3.13`. Verified in the
`app`-only render.

**Impact:** The app package advertises Python versions it never tests against and is
installable on interpreters it may not support.

**Fix:** Use the header-local `python_min` / `python_max` on lines 34 and 38 (they
already exist for exactly this purpose).

---

## 🟠 High

### F3 — Third-party Actions pinned to mutable tags/branches, not commit SHAs
**Category:** Security / supply chain
**Locations:** `template/.github/workflows/{{'' if template_type == 'lib' else '_exclude_'}}pypi-publish.yml.jinja:44` (+ `:19`), and every workflow/action across `.github/` and `template/.github/`

The worst case: `pypa/gh-action-pypi-publish@release/v1` runs in a job holding
`id-token: write` (PyPI trusted publishing) and is pinned to a **branch** (`release/v1`)
— the most mutable ref possible. A compromise of that branch could exfiltrate the OIDC
token and publish arbitrary artifacts under the project's PyPI identity.

Every other third-party action is pinned to a movable **tag**, several running with
write scopes and/or the `easyscience[bot]` token:

- `Rindrics/expect-label-prefix@v1.2.1` — `issues-labels.yml` (`issues: write`)
- `mheap/github-action-required-labels@v5` — `pr-labels.yml` (`pull_request_target`, bot token)
- `enhantica/drafterino@v2` — `release-notes.yml` (`contents: write`, bot token)
- `Mattraks/delete-workflow-runs@v2` — `cleanup.yml` (`actions: write`)
- `softprops/action-gh-release@v3` — `release-notes.yml` (`contents: write`, bot token)
- `codecov/codecov-action@v6`, `prefix-dev/setup-pixi@v0.9.5`

**Impact:** A tag hijack or maintainer-account compromise of any of these runs
attacker code with write scopes (and in several cases the App token) — and because
this is a **template**, the weak pattern is copied into every EasyScience repo. This
is the class of issue behind the `tj-actions/changed-files` incident.

**Fix:** Pin third-party actions to full 40-char commit SHAs with a trailing
`# vX.Y.Z` comment; pin `pypa/gh-action-pypi-publish` to a SHA (PyPA's own
recommendation for trusted publishing). Add Dependabot (`github-actions` ecosystem) to
keep SHAs current (see F22).

### F4 — App `test.yml` references an undefined `PIXI_ENVS`
**Category:** Correctness (drift between lib/app variants)
**Location:** `template/.github/workflows/{{'' if template_type == 'app' else '_exclude_'}}test.yml.jinja:87` (env block `:46-47`)

The **lib** variant defines `PIXI_ENVS` in its env block
(`…lib…test.yml.jinja:48 → 'py-311-env py-313-env'`). The **app** variant was copied
but that line was dropped, while still using it:

```yaml
- uses: ./.github/actions/setup-pixi
  with:
    environments: ${{ env.PIXI_ENVS }}   # resolves to '' for app
```

`${{ env.PIXI_ENVS }}` resolves to empty, so `setup-pixi` receives `environments: ''`.
Worse, the `py-*-env` environments it implies **don't exist** for `app` type — the
template only defines them for `lib` (`pixi.toml.jinja:101-105`).

**Impact:** App CI installs the wrong (or no) environment; the test job is
misconfigured for every generated app repo.

**Fix:** Remove the `environments: ${{ env.PIXI_ENVS }}` override in the app workflow
(let it default), or define `PIXI_ENVS` correctly for app.

### F5 — `pixi` tasks reference tool scripts that don't exist
**Category:** Correctness / broken references
**Locations:** root `pixi.toml:91,106,150,174,210`; `template/pixi.toml.jinja:142,157,203`; `template/tools/`

Root `tools/` contains only `license_headers.py`, yet these tasks call missing scripts
and crash on invocation:

| `pixi.toml` line | Task | Missing script |
| --- | --- | --- |
| 91 / 106 | `nonpy-format-check-modified` / `-fix-modified` | `tools/nonpy_prettier_modified.py` |
| 150 | `notebook-tweak` | `tools/tweak_notebooks.py` |
| 174 | `docs-update-assets` | `tools/update_docs_assets.py` |
| 210 | `github-labels` | `tools/update_github_labels.py` |

`update_docs_assets.py` and `update_github_labels.py` exist under `template/tools/` but
not root `tools/`, so they're broken **in this repo** — and `README.md:329,352` tells
users to run `pixi run github-labels` / `docs-update-assets`.

The **template** ships the same defect to every generated repo:
`template/pixi.toml.jinja:142,157,203` reference `nonpy_prettier_modified.py` and
`tweak_notebooks.py`, which are **not** in `template/tools/`.

**Impact:** Silent foot-guns; anyone running these tasks gets a "No such file" crash.
(None are wired into aggregate `fix`/`check` or CI, which is why it's High, not Highest.)

**Fix:** Add the missing scripts (root can render/copy from `template/tools/`), or
delete the dead tasks.

### F6 — `app` README and all `CONTRIBUTING` files cross-link to the wrong repository
**Category:** Templating correctness (`lib_` vs `app_` confusion)
**Locations:** `template/README.md.jinja:55`; `template/CONTRIBUTING.md.jinja:48,87,95,96,102`

- **README (app branch):** the text *"For the Python library, please see the
  corresponding [library resources]"* links to `{{ app_repo_name }}` — it should be
  `{{ lib_repo_name }}`. The parallel doc `docs/docs/introduction/index.md.jinja:31`
  does this correctly, confirming the intent.
- **CONTRIBUTING:** every repo-specific URL hardcodes `{{ lib_repo_name }}`
  unconditionally (clone URL, `cd`, upstream remote, discussions link) with no
  `template_type` switch. For an **app** repo, contributors are sent to the *library*
  repo; for **app-only**, `lib_repo_name` is a computed default → a nonexistent
  `<name>-lib` repo. Verified in the `both`+`app` and `app`-only renders.

**Fix:** Change `{{ app_repo_name }}` → `{{ lib_repo_name }}` on `README.md.jinja:55`;
add a `template_type → repo_name` header block to `CONTRIBUTING.md.jinja` and use
`repo_name` throughout (as the other templates do).

### F7 — Stale `pixi.lock` + `frozen` CI hides a committed dependency fix
**Category:** Reproducibility / CI integrity
**Locations:** `pixi.lock` (last changed 2026-05-11, commit `866ea01`); `pyproject.toml` (2026-07-02, `190905c`); `pixi.toml` (2026-07-01); `.github/actions/setup-pixi/action.yml:20-23`

`pixi.lock` predates the last `pyproject.toml` change — which **added
`docstring-parser-fork!=0.0.15`** specifically to avoid DOC105 failures (commit
`190905c`, "Exclude docstring-parser-fork 0.0.15") — and the last `pixi.toml` change.
`setup-pixi` defaults to `frozen: true`, so CI installs straight from the stale lock
**without** re-solving and **without** validating it against `pyproject.toml`.

**Impact:** The `docstring-parser-fork` exclusion (and any other post-May dependency
change) is silently **not applied in CI**. Locally, `pixi install` re-solves and
dirties the lock. `locked: true` would have failed loudly the moment the lock drifted.

**Fix:** Regenerate and commit `pixi.lock`. Then switch CI to `locked: true` (see R2)
so future drift fails fast instead of silently using stale pins.

### F8 — Repo has no tests; empty `src/easytemplates/` breaks build/test tasks
**Category:** Quality / correctness
**Locations:** `pyproject.toml:85` (`packages = ['src/easytemplates']`), `pixi.toml:74,79` (`unit-tests`, `test`), `src/easytemplates/` (empty), `tests/` (only empty dirs)

`src/easytemplates/` contains no files (not even `__init__.py`) and `tests/`
(unit/functional/integration) contains no test files, yet `pyproject.toml` declares a
wheel target of `src/easytemplates` and an editable install underpins every task.

**Impact:**
- `pixi run test` → `pytest tests/unit/` collects nothing / errors.
- `pixi run dist-build` / `default-build` fail or emit an empty wheel (hatchling:
  "Unable to determine which files to ship").
- Most importantly, **there is no automated validation of the template itself** — no
  render tests, no tool tests — which is why F1/F2/F4/F5 shipped unnoticed. (The root
  repo has no `test.yml` workflow, so nothing exercises these locally-broken tasks in CI.)

**Fix:** Add `src/easytemplates/__init__.py` (or make the repo explicitly
source-less), and add real tests — at minimum a render-and-check matrix (see R1).

---

## 🟡 Medium

### F9 — `home` ships CI workflows that reference files it never generates
**Category:** Orphaned output (companion to F1)
**Locations:** `template/.github/workflows/test-trigger.yml:38`, `coverage.yml:41,55,69`, `dashboard.yml.jinja:57-66`

These three workflows render for **all** template types. For `home`:
`test-trigger.yml` dispatches `workflow_id: "test.yml"` — which is correctly excluded
for `home`, so the scheduled dispatch 404s; `coverage.yml` / `dashboard.yml` run
`docstring-coverage` / `radon` / `interrogate` against the empty `src/`. Verified: the
`home` render contains these workflows but no `test.yml`.

**Fix:** Exclude `test-trigger.yml`, `coverage.yml`, `dashboard.yml` for
`template_type == 'home'` (same mechanism as F1).

### F10 — `update_docs_assets.py` imports `pooch`, which isn't a dependency
**Category:** Dependency correctness
**Locations:** `template/tools/update_docs_assets.py.jinja:12,53`; `template/pyproject.toml.jinja:41` (`#'pooch'` commented out), dev extras `:45-82` (no `pooch`)

The script does `import pooch` and calls `pooch.retrieve(...)`, but `pooch` is neither a
runtime nor a `dev` dependency (it's a commented-out example runtime dep). So
`pixi run docs-update-assets` — a documented finalize step (`README.md:352`) — fails
with `ModuleNotFoundError: No module named 'pooch'` in a freshly generated project.

Secondary: `main()` catches per-asset exceptions and prints `❌ Failed…`, then
**always** prints `✅ Documentation assets updated successfully!` (`:87`) and exits 0
even if every download failed — masking the exact failure `README.md:336` warns will
break the docs build.

**Fix:** Add `pooch` to the `dev` extras (or vendor the assets); make the script track
failures and exit non-zero when any asset fails.

### F11 — `app` template is a stub: missing entrypoints and broken QML URLs
**Category:** Completeness / correctness
**Locations:** `template/pixi.toml.jinja:301,325,326`; `template/src/.../Gui/Globals/ApplicationInfo.qml.jinja:13-17`; `template/docs/docs/installation-and-setup/index.md.jinja:281-285`, `tutorials/index.md.jinja:24-27`

The app template ships only `<pkg>.qmlproject`, `<pkg>/__init__.py`, and
`<pkg>/Gui/Globals/ApplicationInfo.qml` — but:

- `pixi.toml.jinja` app tasks reference entrypoints that are **never generated**:
  `freeze` and `<name>-py` use `src/<pkg>/main.py`; `<name>-qml` uses
  `src/<pkg>/main.qml`. Both are missing → the app can't be run or frozen from the
  scaffold.
- `ApplicationInfo.qml`:
  - `licenseUrl` (`:15`) = `…/{{ home_repo_name }}/LICENCE` — misspelled **LICENCE**
    (file is `LICENSE`) **and** missing the `/blob/<branch>/` path → 404.
  - `dependenciesUrl` (`:16`) → `…/DEPENDENCIES.md`, which doesn't exist → 404.
  - `version` (`:17`) is hardcoded `'0.1.0'` while the project uses dynamic
    (`versioningit`) versioning → drifts immediately.
  - `homePageUrl`/`issuesUrl` use `home_repo_name` unconditionally (see F18).
- App docs pages are "under development" stubs.

**Impact:** A generated app repo is not runnable/buildable from the template and ships
broken About-box links.

**Fix:** Add `main.py`/`main.qml` scaffolds (or remove the tasks that need them); fix
the QML URLs (`LICENSE`, `blob/<branch>` path, drop `DEPENDENCIES.md` or ship it);
source the QML version dynamically. Alternatively, label the app template experimental
until complete.

### F12 — `pull_request_target` grants write + secrets on fork PRs (fragile)
**Category:** Security
**Locations:** `.github/workflows/pr-labels.yml:11-16,24` and identical `template/.github/workflows/pr-labels.yml`

`pull_request_target` runs in the **base-repo** context with `issues: write` /
`pull-requests: write` and access to `secrets.EASYSCIENCE_APP_KEY`, and triggers on
fork PRs. **Currently safe** — `actions/checkout@v6` (`:24`) specifies no `ref:`, so it
checks out the trusted base commit, and no PR-controlled code is executed. But the
invariant is undocumented and one edit away from a critical secrets-exfiltration hole
(e.g. adding a build/`pixi run` step, or `ref: ${{ github.event.pull_request.head.sha }}`).

**Fix:** Document the invariant ("never check out or execute PR-head code") inline;
prefer dropping the `checkout` step and referencing the bot action by `owner/repo@sha`;
keep permissions this tight.

### F13 — `setup-easyscience-bot` feeds the App ID value into the `client-id` input
**Category:** Correctness (latent)
**Locations:** `.github/actions/setup-easyscience-bot/action.yml:26-29` and identical template copy

`actions/create-github-app-token` exposes two distinct inputs: `app-id` (numeric App
ID) and `client-id` (the App's Client ID string, e.g. `Iv23li…`). The wrapper's input
is named `app-id` and sourced from `vars.EASYSCIENCE_APP_ID`, but it is passed to
`client-id`. Releases apparently work, so the org variable presumably holds the *Client
ID* under a misleading name — a latent footgun for anyone re-provisioning the bot.

**Fix:** Align name and value — rename to `client-id` / `EASYSCIENCE_CLIENT_ID`, or
pass the value to the `app-id` input to match the input's name.

### F14 — `lib_doi` and `app_doi` share an identical placeholder DOI
**Category:** Config / defaults
**Locations:** `copier.yml:141,182`; also `.copier-answers.yml:6`

Both default to `10.5281/zenodo.18163581`. A DOI is unique per Zenodo record; a `both`
project would point its library and app at the same archive. The repo's own answers
file carries this exact placeholder, suggesting it's shipped unchanged.

**Fix:** Use distinct, obviously-fake placeholders (e.g. `10.5281/zenodo.XXXXXXX`) and
add a `validator` requiring the `10.xxxx/…` shape.

### F15 — `pydoclint` & `format-docstring` globally disabled — the CI check verifies nothing
**Category:** CI integrity
**Locations:** `pyproject.toml:315,329`; `template/pyproject.toml.jinja:344,358`

`exclude = '\.'` is a regex where `.` matches any character, so it matches essentially
every path → both tools are effectively disabled everywhere (the inline comment says
"Temporarily disable … until we are ready"). Consequence:
`docstring-lint-check` (root `pixi.toml:86`, the `pixi-docstring-lint-check`
pre-commit hook, and the "Check linting of docstrings" CI step) run `pydoclint` but
check **nothing** — a green check that guarantees nothing. `docstring-format-fix` is
likewise a no-op.

**Fix:** Acceptable as an explicit temporary state, but make it obvious (banner /
`# TODO(#issue)`), and be aware the docstring-lint gate is currently meaningless. When
enabling, replace `'\.'` with a real anchored pattern.

### F16 — Template ships no `.gitattributes`; generated repos get noisy `pixi.lock` merges
**Category:** Templating / hygiene
**Locations:** root `.gitattributes` (exists), `template/` (no `.gitattributes`)

Root has `.gitattributes` with
`pixi.lock merge=binary linguist-language=YAML linguist-generated=true -diff`, but the
template ships none. Every generated project therefore gets 3-way merge conflicts on
`pixi.lock` and shows it in diffs / language stats — exactly what this line prevents.

**Fix:** Add `template/.gitattributes` mirroring the root file.

### F17 — All pre-commit hooks are `stages: [manual]`; `pre-commit-install` is a no-op
**Category:** Tooling
**Locations:** `.pre-commit-config.yaml` (all 7 hooks `manual`); `template/.pre-commit-config.yaml.jinja` (all 8 hooks `manual`); `template/pixi.toml.jinja:252,315`

`pixi run check` works because it passes `--hook-stage manual`. But
`pre-commit-install --hook-type pre-commit --hook-type pre-push` installs git hooks for
stages that **no hook opts into**, so an actual `git commit` / `git push` runs **zero**
checks. The implied safety net doesn't exist. (May be intentional — `pre-commit-setup`
is commented out of `post-install` at `:315` — but then installing those hook types is
misleading.)

**Fix:** Give the fast hooks real `pre-commit` / `pre-push` stages if enforcement is
wanted; otherwise drop the `--hook-type` install so it doesn't imply protection.

### F18 — `mkdocs.yml` uses `home_repo_name` unconditionally (broken for lib/app-only)
**Category:** Templating correctness
**Locations:** `template/docs/mkdocs.yml.jinja:73`; `template/src/.../ApplicationInfo.qml.jinja:13-16`

`home_repo_name` is gated `when: project_type == "both"` (`copier.yml:91`), but the
mkdocs "Main Webpage" social link and the QML About URLs use it unconditionally. For
lib-only/app-only it survives only via its computed default, producing a link to a
"home" repo that doesn't exist (verified `app`-only → `…/easyscience/apponly`).

**Fix:** For non-`both` projects, point these at the current `repo_name`, or guard with
`{% if project_type == "both" %}`.

### F19 — No `_min_copier_version` / `_envops`; bugs are masked by lenient undefined
**Category:** Copier config
**Location:** `copier.yml:191-193`

No `_min_copier_version` is set, though the template relies on modern behaviors
(`to_nice_yaml`, `strftime`, `_copier_conf.answers_file`, negative-index slicing) and
on Copier's **default lenient-undefined** handling — which is the only reason F2, F6,
F18 render at all instead of crashing. No `_envops` documents this reliance.

**Fix:** Add `_min_copier_version` (e.g. `'9.0.0'` or your tested floor). After fixing
F2/F6/F18, consider `_envops: {undefined: strict}` so future variable mistakes fail
loudly instead of rendering empty strings.

### F20 — Root `CONTRIBUTING.md` references a nonexistent `pixi run spdx-add`
**Category:** Docs
**Location:** `CONTRIBUTING.md:253`

The doc says *"To add missing license headers: `pixi run spdx-add`"*, but no such task
exists — the task is `license-add` (`pixi.toml:217`).

**Fix:** Change `spdx-add` → `license-add`.

### F21 — Repo's own `.copier-answers.yml` `_commit` is two releases stale
**Category:** Hygiene
**Location:** `.copier-answers.yml:3`

`_commit: v0.11.2-6-gf130ad5` while the repo is at `v0.13.1-4-g190905c` (v0.11.3,
v0.11.4, v0.12.0, v0.13.0, v0.13.1 released since). The repo self-applies its own
template but hasn't been re-copied since v0.11.2, so drift between `template/` and the
root's generated files (F5, F34) has accumulated.

**Fix:** Run `copier update` on the repo itself (dogfooding) and commit the refreshed
answers; or explicitly document the root as a hand-maintained render.

---

## 🔵 Low

### F22 — No Dependabot/Renovate configuration
**Category:** Maintainability
**Locations:** none present in `.github/` or `template/.github/`

There is no automated dependency-update config for GitHub Actions or Python deps. This
compounds F3 (SHA-pinned actions need automated bumps to stay current) and F7 (lock
drift).

**Fix:** Add `.github/dependabot.yml` (and a templated one) for the `github-actions`
and `pip` ecosystems.

### F23 — No `SECURITY.md`, `CODEOWNERS`, or issue/PR templates shipped
**Category:** Governance
**Locations:** none in `.github/` or `template/.github/`

`CONTRIBUTING.md:426` has an informal "Security Issues" section but there's no
`SECURITY.md` (GitHub's "Report a vulnerability" entry point), no `CODEOWNERS` (to
enforce review routing), and no issue/PR templates. Some may exist at the org
`.github` level, but the template ships none.

**Fix:** Add templated `SECURITY.md`, `CODEOWNERS`, and `ISSUE_TEMPLATE`/
`PULL_REQUEST_TEMPLATE`, or document that they are intentionally org-level.

### F24 — Docs claim `pixi run check` runs unit tests; root config's hook set doesn't
**Category:** Docs / drift
**Locations:** `CONTRIBUTING.md:233`, `README.md:420`; `.pre-commit-config.yaml` (no `pixi-unit-tests` hook)

Both docs show `unit-tests … Passed` in the expected `pixi run check` output, but the
root pre-commit config — unlike `template/.pre-commit-config.yaml.jinja:60-65` — has no
`pixi-unit-tests` hook, so root `check` never runs tests. (Consistent with F8: the root
has no tests.)

**Fix:** Align the doc with the root's actual hook set, or add the hook once F8 is fixed.

### F25 — `github.head_ref` flows into unquoted shell paths
**Category:** Security (low risk)
**Locations:** `template/.github/workflows/dashboard.yml.jinja:16,45-53`, `docs.yml.jinja:51`, plus every `CI_BRANCH: ${{ github.head_ref || github.ref_name }}`

The attacker-controllable PR branch name reaches shell as `CI_BRANCH` and is used
unquoted (`../$BRANCH`, `origin/$BRANCH`, `mkdir -p …/${CI_BRANCH}`). Risk is low — it's
passed via an **env var** (the recommended safe pattern, not `${{ }}` inside `run:`),
and Git refname rules forbid the dangerous metacharacters — but a `/` in a branch name
can still create unexpected nested paths.

**Fix:** Quote expansions (`"../$BRANCH"`) and sanitize `CI_BRANCH` (replace `/`→`-`)
before using it as a filesystem path.

### F26 — `docs.yml` hardcodes `-lib` in the artifact name for all types
**Category:** Templating
**Location:** `template/.github/workflows/docs.yml.jinja:141`

`name: site-local_{{ project_name | lower }}-lib-${{ env.RELEASE_VERSION }}` is
ungated, so an **app** repo's docs artifact is mislabeled `…-lib-…` (while the
notebook steps at `:108-125` are correctly gated on `template_type == "lib"`).

**Fix:** Use `-{{ template_type }}` (or drop the suffix).

### F27 — `.badgery.yaml.jinja` mixes `file:` and `workflow:` keys
**Category:** Config
**Locations:** `template/.badgery.yaml.jinja:8,15,21` (`file:`) vs `:70,77` (`workflow:`)

`gh_action` badge cards use `file:` for the Tests group but `workflow:` for the
Build & Release group. Only one key is correct per Badgery's schema; the other badges
likely render blank/broken.

**Fix:** Verify Badgery's expected key and use it consistently.

### F28 — `master` ruleset requires 0 approvals and no status checks
**Category:** Governance
**Location:** `.github/configs/rulesets-master.json` (and identical template copy)

The `master` branch ruleset sets `required_approving_review_count: 0`,
`require_code_owner_review: false`, and defines **no** required status checks — so
anyone with write access can merge to the "stable releases only" branch without review
or green CI. Likely intentional to permit the automated release-PR flow, but worth an
explicit decision.

**Fix:** If review isn't required by design, document why; otherwise require ≥1 approval
and/or required status checks (with a bypass for the release bot).

### F29 — README duplicate section titles and broken ordered-list numbering
**Category:** Docs
**Locations:** `README.md:33,36` (two "Push Changes to the Repository": §2.7 and §2.10), `:537,543` (two `1.` items in Step 4)

Two sections share the identical title (the TOC anchors collide), and the Step-4 list
restarts at `1.` after a code block instead of continuing to `2.`

**Fix:** Give the sections distinct titles; renumber the list.

### F30 — `release-pr.yml` interpolates `${{ env.SOURCE_BRANCH }}` inside `run:`
**Category:** Security (low risk)
**Location:** `.github/workflows/release-pr.yml:47-53`

`SOURCE_BRANCH` (from a `workflow_dispatch` input) is set in `env:` but then
re-interpolated as `${{ env.SOURCE_BRANCH }}` directly inside the `gh pr create` `run:`
block rather than referenced as the shell var `$SOURCE_BRANCH`. Low risk (only
maintainers can dispatch), but it's the exact pattern a template should model
correctly.

**Fix:** Reference `"$SOURCE_BRANCH"` / `"$DEFAULT_BRANCH"` from the shell instead of
`${{ … }}` interpolation.

### F31 — `pypi-test.yml` has a dead `pull_request` concurrency reference
**Category:** Correctness (cosmetic)
**Location:** `template/.github/workflows/{{'' if template_type == 'lib' else '_exclude_'}}pypi-test.yml.jinja:13`

The concurrency group uses `github.event.pull_request.number || github.ref`, but the
workflow triggers only on `schedule`/`workflow_dispatch`, so the first operand is always
empty. Misleading copy-paste.

**Fix:** Simplify to `group: ${{ github.workflow }}-${{ github.ref }}`.

---

## ⚪ Lowest

### F32 — Pinned Actions are one version behind
**Category:** Maintenance
**Locations:** `actions/setup-pixi/action.yml:36` (`@v0.9.5`, latest `v0.10.0`); `checkout@v6` (latest `v7`); `codecov-action@v6` (latest `v7`), across all workflows

Not broken, but drifting behind. Best bumped together with the SHA-pinning in F3 and
Dependabot in F22.

### F33 — `coverage.yml` job comments are mislabeled
**Category:** Maintainability
**Location:** `template/.github/workflows/coverage.yml:66`

Jobs are labeled `# Job 1`, `# Job 2`, `# Job 4` (no Job 3), and the file's header
narrative is a leftover copied from `test.yml`. Cosmetic.

**Fix:** Renumber/rewrite the comments to match actual jobs.

### F34 — Root runs `notebook-lint-check` in CI but has no notebooks
**Category:** CI (drift)
**Locations:** `.github/workflows/lint-format.yml:88-92`; `pixi.toml:87` (`nbqa ruff template/`)

The root `lint-format.yml` runs `notebook-lint-check` unconditionally (the template
gates it behind `template_type == "lib"`). `nbqa ruff template/` finds no real
notebooks under `template/` (only `…tutorial.ipynb.jinja`), so it's a wasted step — a
symptom of the stale self-render (F21).

**Fix:** Drop the step/hook in the root repo, or re-copy from the current template.

### F35 — Dead/unused Jinja `set` variables in some templates
**Category:** Cleanliness
**Locations:** e.g. `template/docs/docs/index.md.jinja:1-5` (`current_type` set, never used)

Minor unused `{% set %}` bindings left over from refactors.

**Fix:** Remove unused variables.
