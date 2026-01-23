# EasyScience Copier Templates

This repository provides Copier templates used to create, structure, and
maintain repositories under the EasyScience organization.

It is intended primarily for developers and contributors. The templates 
enforce organization-wide standards for:

- repository layout,
- CI/CD workflows,
- documentation structure,
- code quality tooling,
- release automation.

All templates are based on [Copier](https://copier.readthedocs.io/),
which allows projects to stay synchronized with upstream template
updates over time.

---


## 📋 Table of Contents

- [Overall Project Structure](#-overall-project-structure)
- [Step 1: Create GitHub Repositories](#-step-1-create-github-repositories)
  - [1.1. Create and Set Up New Repositories](#11-create-and-set-up-new-repositories)
- [Step 2: Initialize Projects Using Copier](#-step-2-initialize-projects-using-copier)
  - [2.1. Clone Repositories](#21-clone-repositories)
  - [2.2. Set Up Pixi](#22-set-up-pixi)
  - [2.3. Install Copier](#23-install-copier)
  - [2.4. Generate Project Description (Home Repository)](#24-generate-project-description-home-repository)
  - [2.5. Generate Library / Application Repositories](#25-generate-library--application-repositories)
  - [2.6. Where Are Answers Stored?](#26-where-answers-are-stored)
  - [2.7. Push Changes to the Repository](#27-push-changes-to-the-repository)
  - [2.8. Finalize Project Setup](#28-finalize-project-setup)
  - [2.8. Code Quality Checks](#28-code-quality-checks)
  - [2.9. Push Changes to the Repository](#29-push-changes-to-the-repository)
- [Step 3: Post-Initialization Repository Setup](#-step-3-post-initialization-repository-setup)
  - [3.1. Create develop Branch](#31-create-develop-branch)
  - [3.2. About gh-pages Branch and Pages Activation](#32-about-gh-pages-branch-and-pages-activation)
  - [3.3. Set Repository Labels](#33-set-repository-labels)
  - [3.4. Add Repository Secrets](#34-add-repository-secrets)
  - [3.5. Set Branch Protection Rules](#35-set-branch-protection-rules)
- [Step 4: Updating Existing Repositories](#-step-4-updating-existing-repositories)
  - [To update the repository with template changes](#to-update-the-repository-with-template-changes)
  - [Using a Specific Version/Tag](#using-a-specific-versiontag)
  - [GitHub Actions Workflows](#github-actions-workflows)
- [Release Workflow](#-release-workflow)

## 🧱 Overall Project Structure

EasyScience projects typically consist of multiple repositories:

1. Home (umbrella) repository. Example: `easyscience/peasy`
   - Acts as the entry point for the project
   - Stores the project description file (Copier answers)
2. Library repository (if applicable). Example: `easyscience/peasy-lib`
   - Contains the Python library
   - Uses shared metadata from the home repository
3. Application repository (if applicable). Example:
   `easyscience/peasy-app`
   - Contains the GUI application
   - Uses the same shared project metadata

The home repository is created first, because it defines metadata reused
by the others.

## 🚀 Step 1: Create GitHub Repositories

Before running Copier, repositories must exist on GitHub.

### 1.1. Create and Set Up New Repositories

To create a new repository:

1. Go to
   [GitHub: Create New Repository](https://github.com/organizations/easyscience/repositories/new).
2. **Repository template:** Select "No template" (Copier templates will
   be used instead).
3. **Repository name:** Enter a name, e.g., `peasy`.
4. **Description:** Use the
   [EasyScience organization profile](https://github.com/easyscience/.github/blob/master/profile/README.md)
   for inspiration. If needed, update the org profile first.
5. **Visibility:** Set to **Public**.
6. **Do not initialize** with README, `.gitignore`, or license (Copier
   will handle these).
7. Click **Create repository**.

Depending on your project, repeat the same steps for additional
repositories as needed:

- For libraries: `peasy-lib`
- For applications: `peasy-app`

---

## 🛠️ Step 2: Initialize Projects Using Copier

### 2.1 Clone Repositories

Clone all related repositories locally:

```bash
git clone https://github.com/easyscience/peasy.git
git clone https://github.com/easyscience/peasy-lib.git
git clone https://github.com/easyscience/peasy-app.git
```

### 2.2. Set Up Pixi

We use [**Pixi**](https://prefix.dev) for dependency management and
project configuration. See the
[Pixi installation guide](https://pixi.prefix.dev/latest/installation/)
for details.

Navigate into the home repository (e.g., `peasy`) and initialize a new
Pixi project:

```bash
cd peasy
```

```bash
pixi init
```

```bash
pixi install
```

### 2.3. Install Copier

Install Copier inside the Pixi environment:

```bash
pixi add copier
```

### 2.4 Generate Project Description (Home Repository)

> **Note:** This step generates only the project metadata, not code or
> structure.

```bash
pixi run copier copy gh:easyscience/templates . --data template_type=home --exclude '**/*' --exclude '!{{_copier_conf.answers_file}}' --exclude '!.gitignore'
```

Fill in the required information when prompted. For project name, alias,
and short description, refer to the organization profile for
consistency.

> **Important:** These answers are stored in a project description file
> `.copier-answers.yml`, which becomes the single source of truth for
> all related repositories.
>
> Do not modify it manually. Instead, update answers by re-running
> Copier in the home repository when needed.

Commit and push:

```bash
git add -A
git commit -m "Initial project description file using Copier templates"
git push origin master
```

Navigate back to the parent directory:

```bash
cd ..
```

### 2.5 Generate Library / Application Repositories

Now, set up Pixi and Copier for the library or application repository.
In the example below, we use the library repository (e.g., `peasy-lib`).
In case of an application, replace with the application repository name
(e.g., `peasy-app`):

Navigate to the target repository:

For library:
```bash
cd peasy-lib
```

For application:
```bash
cd peasy-app
```

Initialize Pixi and install Copier:
```bash
pixi init
```

```bash
pixi install
```

```bash
pixi add copier
```

Apply the Copier templates to generate the project structure.

> **Important:** Use the `--data-file` option to provide the path to the
> `.copier-answers.yml` file with answers created in the main repository
> (`peasy`). 

For library:
```bash
pixi run copier copy gh:easyscience/templates . --data-file ../peasy/.copier-answers.yml --data template_type=lib
```

For application:
```bash
pixi run copier copy gh:easyscience/templates . --data-file ../peasy/.copier-answers.yml --data template_type=app
```

> **Note:** When prompted with `conflict. overwrite pixi.toml?` or 
> `conflict. overwrite .gitignore?` confirm with `Yes` to overwrite the 
> configuration files created during `pixi init`.


### 2.6. Where Are Answers Stored?

The answers needed to fill in the library templates are automatically
taken from the home repository and stored locally in
`peasy-lib/.copier-answers.yml` or `peasy-app/.copier-answers.yml`.

They are autogenerated by Copier and should not be modified manually.

### 2.7. Push Changes to the Repository

After generating the project structure, **push the changes** to GitHub:

```bash
git add -A
git commit -m "Initial project setup using Copier templates"
git push origin master
```

### 2.8. Finalize Project Setup

After the project structure is generated, run the following commands to
finalize the setup:

- **Reinstall default environment:** This step ensures that all
  dependencies are correctly installed as per new `pixi.toml`
  configuration.

  ```bash
  pixi reinstall
  ```

- **Install extra development dependencies and set up tools:** This step
  sets up pre-commit hooks, installs additional development
  dependencies, and configures non-Python file formatting. See,
  `pixi.toml` for details regarding the `post-install` task.

  ```bash
  pixi run post-install
  ```

- **Update documentation assets:** Updates the logo and other assets in
  the `docs/` folder. Run this every time you update project-related
  logos or assets, especially after changes in the
  `easyscience/assets-branding` repository. See, `pixi.toml` for details
  regarding the `post-install` task.

  ```bash
  pixi run docs-update-assets
  ```

- **Update SPDX license headers:** Updates license headers in all
  project files. Run this whenever the copyright year changes, new files
  are added, or license information needs to be refreshed. See,
  `pixi.toml` for details regarding the `post-install` task.

  ```bash
  pixi run spdx-update
  ```

- **Format all project files:** Ensures all files adhere to the
  project's coding standards as defined in `pyproject.toml`. Run this
  after any changes to source code, configuration, workflows, or docs.
  See, `pixi.toml` for details regarding the `post-install` task.
  ```bash
  pixi run fix
  ```

> **Tip:** Run `pixi run fix` every time after updating any template
> files or modifying any project files (source code, configuration,
> workflows, docs, etc.) to ensure consistent formatting.
> 
> Normally, after running `pixi run fix`, you should see the message
> `✅ All code auto-formatting steps have been applied.` indicating that 
> all steps in the auto-formatting pipeline were successfully executed.
> If you do not see this message, try running the command again.
> 
> Note, that even if you see this message, there might still be some 
> issues left, which need to be fixed manually. In such cases, refer to
> the output of `pixi run pre-commit-check` or `pixi run pre-push-check`
> commands described below.

### 2.8. Code Quality Checks

Templates set up pre-commit and pre-push hooks to ensure code quality.
These hooks automatically check for code formatting, linting, and other
quality standards before allowing commits or pushes.

If you see `commit failed` or `push failed` from pre-commit/pre-push
hooks, fix the issues reported by those hooks, commit again, and push
again.

To check issues reported by pre-commit hooks without committing, run:

First, stage all changes:
```bash
git add -A
```

Then, either check if commit would succeed:
```bash
pixi run pre-commit-check
```

or check if push would succeed:
```bash
pixi run pre-push-check
```

Often, running `pixi run fix` is enough to fix issues automatically. And
sometimes, one needs to run it twice to fix all issues. If issues
persist, manually address them based on the output of the above commands.

#### Disable Hooks Temporarily

If you need to disable pre-commit or pre-push hooks temporarily (not
recommended), run:

```bash
pixi run pre-commit-uninstall
```

To re-enable them, run:

```bash
pixi run pre-commit-install
```

> **Tip:** To fine-tune which checks are performed by pre-commit hooks,
> modify the configuration in the `.pre-commit-config.yaml` file located
> at the project root. 
> 
> After modifying this file, reinstall the hooks using the commands 
> above.

> **Note:** If pre-commit or pre-push hooks are too slow, try disabling
> the slowest check of the non-Python files formatter Prettier executed
> in both pre-commit ('pixi-nonpy-format-check-modified') and pre-push 
> ('pixi-nonpy-format-check') hooks. To do this, open the 
> `.pre-commit-config.yaml` file and temporarily comment out or remove 
> them. 

### 2.9. Push Changes to the Repository

After generating the project structure, **push the changes** to GitHub:

```bash
git add -A
git commit -m "..."
git push origin master
```

---

## 🛡️ Step 3: Post-Initialization Repository Setup

After you have made your initial commit and pushed to GitHub, complete
the following steps:

### 3.1. Create develop Branch

Create and push the develop branch:

```bash
git checkout -b develop
git push -u origin develop
```

### 3.2. About gh-pages Branch and Pages Activation

The `gh-pages` branch will be created automatically by
[mike](https://github.com/jimporter/mike) when you first deploy
documentation. Do not attempt to activate GitHub Pages until this branch
exists.

Once `gh-pages` exists, activate Pages deployment:

- Go to
  [GitHub Pages settings](https://github.com/easyscience/peasy-lib/settings/pages)
- In "Build and deployment" select **Source:** Deploy from a branch
- In **Branch** select `gh-pages` and click **Save**

> **Note:** Activating Pages deployment will add a workflow "pages build
> and deployment", which will be automatically triggered by
> `github-pages[bot]` after mike pushes a new version of docs to
> `gh-pages`.
>
> **Docs versioning:** Every new version of the documentation (built
> site) will be published under a dedicated directory named after the
> new release tag and added to the `gh-pages` branch. This allows users
> to access documentation for each release at a unique URL.

### 3.3. Set Repository Labels

Ensure correct labels, including the bot label
([see ADR](https://github.com/orgs/easyscience/discussions/33),
[example](https://github.com/easyscience/peasy-lib/labels)).

### 3.4. Add Repository Secrets

Add repository secrets (e.g., API keys, deployment keys):

- The `easyscience[bot]` GitHub App should have access automatically
  (configured at the org level). Add it to the `develop` bypass
  protection rules for automatic backmerge after new releases.
- Add the PyPI API token secret for library repositories (for publishing
  to PyPI). Confirm if this is set at the org level.

### 3.5. Set Branch Protection Rules

Set branch protection rules
([GitHub Rules Settings](https://github.com/easyscience/peasy-lib/settings/rules))
only after the relevant branches exist:

- Create ruleset **"master branch protection"** with:
  - Enforcement status: Active
  - Branch targeting criteria: Add target → include default branch
  - Restrict deletions: ✔️
  - Require a pull request before merging: ✔️ (Allowed merge methods:
    Merge only)
  - Block force pushes: ✔️
  - Click "Save changes" button
- Create ruleset **"develop branch protection"** with:
  - Enforcement status: Active
  - Branch targeting criteria: Add target → include by pattern → develop
  - Restrict deletions: ✔️
  - Require a pull request before merging: ✔️ (Allowed merge methods:
    Squash only)
  - Block force pushes: ✔️
  - Click "Save changes" button
- Create ruleset **"gh-pages branch protection"** with:
  - Enforcement status: Active
  - Branch targeting criteria: Add target → include by pattern →
    gh-pages
  - Restrict deletions: ✔️
  - Block force pushes: ✔️
  - Click "Save changes" button

---

## 🔄 Step 4: Updating Existing Repositories

When templates evolve, existing repositories must be updated.

### 📌 To update the repository with template changes:

1. Go to the project directory, e.g., `peasy-lib`:

```bash
cd peasy-lib
```

2. Apply updated templates:

```bash
pixi run copier-update
```

If conflicts arise, Copier will prompt you to review them.

Sometimes, one need to run Copier recopy instead of update, or even redo
a standard copy again (see
[Copier docs](https://copier.readthedocs.io/en/stable/generating/#regenerating-a-project)
for details).

This can be dony by:

```bash
pixi run copier-recopy
```

or in case of redoing a standard copy again:

```bash
pixi run copier-copy
```

#### Using a Specific Version/Tag

To update to a specific version or tag of the templates (instead of the
default latest tagged release), specify the version in the Copier
command. This is useful for testing updates before official release:

```bash
pixi run copier-update --vcs-ref=master
```

If conflicts arise, Copier will prompt you to review them.

### GitHub Actions Workflows

Templates include a set of GitHub Actions workflows for CI/CD, testing,
documentation building, and release management. Check the
`.github/workflows/` directory for available workflows and their
configurations.

## 🚀 Release Workflow

Follow these steps to create a new release and manage the release
process:

1. Merge feature branches to develop as described in
   [ADR 12](https://github.com/orgs/easyscience/discussions/12).
2. To create an automated PR from develop to master for a new release,
   manually run the Release PR workflow from the Actions tab via the
   "Run workflow" button.
3. No need to manually set the package version. It is automatically
   suggested from PR labels (features → develop). Ensure correct PR
   labels and titles, as these are used to generate draft release notes.
4. After merging develop to master and creating a draft release, check
   that all release notes and the suggested tag/version are correct.
   Publish the release by clicking "Publish release". This triggers
   documentation site build, auto backmerge from tagged master to
   develop for version bumping, and PyPI publishing (for libraries).
