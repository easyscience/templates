# Recommendations — `easyscience/templates`

Improvements beyond the individual bug fixes in [`findings.md`](findings.md). These are
grouped by theme and ordered roughly by leverage. Each notes the findings it addresses.

---

## Testing & self-validation

### R1 — Add a render-and-check CI matrix (highest leverage)
*Addresses the root cause of F1, F2, F4, F5, F8, F9, F18 and prevents the whole class.*

The single biggest gap is that **nothing validates the template's own output.** Add a
CI job that, for a matrix of `{lib, app, home}` × representative `project_type` values:

1. runs `copier copy . <dst> --data-file <fixture-answers> --defaults`,
2. asserts the render succeeds **with `--envops strict`** (or a temporary strict run)
   so undefined variables fail instead of rendering empty,
3. runs `pixi install` + `pixi run check` inside the generated project,
4. optionally builds the wheel / serves the docs.

Store a few answer fixtures under `tests/fixtures/`. This would have caught F1
(`home` broken), F2 (wrong Python), F4 (`PIXI_ENVS`), and F5 (missing scripts) before
release. Pair with `pytest` cases that assert specific invariants (e.g. "an `app`
render's `pyproject.toml` has `requires-python = '>=3.13'`", "no file named
`_exclude_*` exists in output", "every `pixi` task's script file exists").

### R2 — Make CI fail on lock drift; keep the lock fresh
*Addresses F7.*

Switch `setup-pixi`'s default from `frozen: true` to **`locked: true`** so CI fails the
moment `pixi.lock` and `pyproject.toml` disagree (instead of silently installing stale
pins). Add a scheduled job (or Dependabot, R6) that runs `pixi lock` and opens a PR when
the lock changes. Regenerate and commit the current lock now.

### R3 — Give the root repo a real (even minimal) test suite
*Addresses F8.*

Add `src/easytemplates/__init__.py` (or convert the repo to an explicitly source-less
"tooling" repo and adjust the hatchling target). Add unit tests for the shipped scripts
(`license_headers.py`, `update_github_labels.py`, `update_docs_assets.py`) — they're
non-trivial and currently untested — and wire a `test.yml` workflow so `pixi run test`
actually runs in CI.

---

## Templating robustness

### R4 — Eliminate the `lib_`/`app_` variable-confusion class
*Addresses F2, F6, F11, F18 and future recurrences.*

The recurring root cause is files reaching past the header-normalized locals
(`repo_name`, `package_name`, `python_min/max`) to the raw `lib_*`/`app_*`/`home_*`
questions. Two structural fixes:

- **Centralize the header block** (`template_type → repo_name/package_name/…`) into a
  single Jinja macro or `_copier_conf`-included partial, imported by every template,
  so the mapping is defined once and files can only use the normalized locals.
- **Turn on strict undefined** (`_envops: {undefined: strict}` in `copier.yml`) *after*
  fixing F2/F6/F18 — this converts silent empty-string bugs into loud render failures,
  and combined with R1 makes the whole class un-shippable.

### R5 — Harden `copier.yml` questions
*Addresses F14; general robustness.*

- Add `_min_copier_version` (F19).
- Add `validator:` clauses: `project_contact_email` (email shape),
  `lib_doi`/`app_doi` (`^10\.\d{4,}/.+`), `lib_package_name`/`app_package_name`
  (lowercase Python identifier), `project_shortcut` (2–3 chars).
- Replace shared/real placeholder DOIs with obvious sentinels (`zenodo.XXXXXXX`).
- Consider a `migrations`/`_tasks` section if future template updates need data
  transforms.

---

## Supply-chain & security hardening

### R6 — Pin actions to SHAs + add Dependabot
*Addresses F3, F22, F32.*

Pin **all** third-party actions to full commit SHAs with a `# vX.Y.Z` comment; do this
first for the OIDC-privileged `pypa/gh-action-pypi-publish`. Add `.github/dependabot.yml`
(and a templated copy) for the `github-actions` and `pip` ecosystems so pins stay
current without manual toil. This is especially important because the template
propagates its CI patterns to every org repo.

### R7 — Document and fence the privileged-workflow invariants
*Addresses F12, F13, F25, F30.*

- Add an inline comment to `pr-labels.yml` stating it must **never** check out or
  execute PR-head code, and prefer referencing the bot action by `owner/repo@sha` over
  a `checkout`.
- Fix the `client-id`/`app-id` naming mismatch in `setup-easyscience-bot` so the token
  provisioning is self-documenting.
- Use shell variables (`"$SOURCE_BRANCH"`), quoting, and `/`→`-` sanitization anywhere a
  branch name reaches shell.

### R8 — Add standard governance files
*Addresses F23, F28.*

Ship templated `SECURITY.md`, `CODEOWNERS`, and issue/PR templates (or document that
they're intentionally provided at the org `.github` level). Revisit the `master`
ruleset's 0-approval / no-status-check policy and record the decision.

---

## Tooling & developer experience

### R9 — Resolve the "checks that check nothing" gaps
*Addresses F15, F17.*

- Either enable `pydoclint`/`format-docstring` (replace `exclude = '\.'` with a real
  pattern) or remove their CI steps/hooks so a green check reflects reality. Track the
  "enable docstring linting" work in a tracked issue rather than an open-ended
  "temporarily".
- Decide the pre-commit story: give fast hooks real `pre-commit`/`pre-push` stages for
  on-commit enforcement, or stop installing those hook types so the setup doesn't imply
  protection it doesn't provide.

### R10 — Fix or remove broken/missing tooling
*Addresses F5, F10, F16.*

- Ship the referenced scripts (`nonpy_prettier_modified.py`, `tweak_notebooks.py`) or
  delete the dead `pixi` tasks — in both root and template.
- Add `pooch` to the `dev` extras (or vendor branding assets) and make
  `update_docs_assets.py` exit non-zero on failure instead of always printing success.
- Add `template/.gitattributes` so generated repos get the same `pixi.lock` merge
  treatment as this one.

### R11 — Single-source duplicated files
*Reduces drift (F21, F34).*

`tools/license_headers.py` is a byte-identical copy of `template/tools/license_headers.py`;
`prettierrc.toml` is duplicated too. Where a file must exist in both root and template,
prefer generating the root copy from the template (dogfooding via `copier update`, R12)
rather than maintaining parallel copies that silently drift.

### R12 — Dogfood the template on itself
*Addresses F21, F34, and drift generally.*

Re-run `copier update` on this repo so `.copier-answers.yml._commit` tracks HEAD and the
root's generated files match the current `template/`. Making "the templates repo is a
clean render of its own `lib` template, plus tooling" an invariant (checked in CI) turns
drift into a test failure.

---

## Documentation polish

### R13 — Correct and de-duplicate the docs
*Addresses F20, F24, F29, F11 (app docs).*

- `CONTRIBUTING.md`: `spdx-add` → `license-add`; align the sample `check` output with
  the repo's actual hook set.
- `README.md`: give the two "Push Changes" sections distinct titles; fix the Step-4
  ordered-list numbering.
- Complete the "under development" app docs (installation, tutorials) or clearly mark
  the app template as experimental until F11 is resolved.
- Consider a short `docs/` note distinguishing "instructions for using the templates"
  (this repo's README) from "what generated repos contain," since several doc snippets
  describe generated-project tasks that don't exist in this repo.

---

## Suggested sequencing

1. **Now (correctness):** F1, F2, F5, F6, F7 → then R1 (render-and-check CI) so they
   can't regress.
2. **Next (safety net):** R2, R4 (strict undefined + centralized header), R6 (SHA pins +
   Dependabot).
3. **Then (integrity & DX):** R3, R9, R10, R12.
4. **Ongoing (polish/governance):** R5, R7, R8, R11, R13.
