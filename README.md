# EasyScience Copier Templates

This repository provides Copier templates used to create, structure, and maintain repositories under the EasyScience organization.

It is intended primarily for developers and contributors, especially those who:
	•	create new EasyScience projects,
	•	maintain existing repositories,
	•	contribute to CI, tooling, documentation, or release workflows.

The templates enforce organization-wide standards for:
	•	repository layout,
	•	CI/CD workflows,
	•	documentation structure,
	•	code quality tooling,
	•	release automation.

All templates are based on [Copier](https://copier.readthedocs.io/)￼, which allows projects to stay synchronized with upstream template updates over time.

---

## 📋 Table of Contents

- [Available Templates](#available-templates)
- [Step 1: Create New Repositories](#step-1-create-new-repositories)
- [Step 2: Apply Templates and Initialize Projects](#step-2-apply-templates-and-initialize-projects)
  - [2.1. Clone All Repositories Locally](#21-clone-all-repositories-locally)
  - [2.2. Set Up Pixi](#22-set-up-pixi)
  - [2.3. Install Copier](#23-install-copier)
  - [2.4. Generate the Project Description File (Main Repository)](#24-generate-the-project-description-file-main-repository)
  - [2.5. Generate the Project Structure (lib/app Repository)](#25-generate-the-project-structure-libapp-repository)
  - [2.6. Where Are Answers Stored?](#26-where-are-answers-stored)
  - [2.7. Push Changes to the Repository](#27-push-changes-to-the-repository)
  - [2.8. Code Quality Checks](#28-code-quality-checks)
- [Step 3: Post-Initialization Repository Setup](#step-3-post-initialization-repository-setup)
  - [3.1. Create develop Branch](#31-create-develop-branch)
  - [3.2. About gh-pages Branch and Pages Activation](#32-about-gh-pages-branch-and-pages-activation)
  - [3.3. Set Repository Labels](#33-set-repository-labels)
  - [3.4. Add Repository Secrets](#34-add-repository-secrets)
  - [3.5. Set Branch Protection Rules](#35-set-branch-protection-rules)
- [Step 4: Keep Your Repository Updated](#step-4-keep-your-repository-updated)
- [FAQ & Troubleshooting](#faq--troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Release Workflow](#release-workflow)

## 🏗️ Available Templates

| Template  | Description | Source Repository |
|-----------|-------------|------------------|
| `shared`  | Shared base template with common files (CI workflows, licensing, etc.) | [easyscience/templates-shared](https://github.com/easyscience/templates-shared) |
| `lib`     | Python library template (e.g., diffraction-lib) | [easyscience/templates-lib](https://github.com/easyscience/templates-lib) |
| `app`     | Qt QML desktop application template (e.g., diffraction-app) | [easyscience/templates-app](https://github.com/easyscience/templates-app) |

---

### Template layering

Templates are applied incrementally:
```
shared → lib / app
```

•	shared defines organization-wide defaults.
•	lib / app add project-type-specific files.
•	This separation allows updating shared infrastructure without touching project-specific logic.

## 🧱 Overall Project Structure

EasyScience projects typically consist of multiple repositories:

1. Home (umbrella) repository

Example: easyscience/peasy
	•	Acts as the entry point for the project
	•	Hosts the project website / landing page
	•	Stores the project description file (Copier answers)
	•	Does not contain implementation code

2. Library repository (if applicable)

Example: easyscience/peasy-lib
	•	Contains the Python library
	•	Publishes documentation and PyPI packages
	•	Uses shared metadata from the home repository

3. Application repository (if applicable)

Example: easyscience/peasy-app
	•	Contains the GUI application
	•	Uses the same shared project metadata

The home repository is created first, because it defines metadata reused by the others.

## 🚀 Step 1: Create GitHub Repositories

Before running Copier, repositories must exist on GitHub.

Repository creation guidelines

### 1.1. Create and Set Up New Repositories

To create a new repository:

1. Go to [GitHub: Create New Repository](https://github.com/organizations/easyscience/repositories/new).
2. **Repository template:** Select "No template" (Copier templates will be used instead).
3. **Repository name:** Enter a name, e.g., `peasy`.
4. **Description:** Use the [EasyScience organization profile](https://github.com/easyscience/.github/blob/master/profile/README.md) for inspiration. If needed, update the org profile first.
5. **Visibility:** Set to **Public**.
6. **Do not initialize** with README, `.gitignore`, or license (Copier will handle these).
7. Click **Create repository**.

Depending on your project, repeat the same steps for additional repositories as needed:
   - For libraries: `peasy-lib`
   - For applications: `peasy-app`


---







## 🛠 Step 2: Initialize Projects Using Copier

### 2.1 Clone Repositories

Clone all related repositories locally:

```bash
git clone https://github.com/easyscience/peasy.git
git clone https://github.com/easyscience/peasy-lib.git
git clone https://github.com/easyscience/peasy-app.git
```

### 2.2. Set Up Pixi

We use [**Pixi**](https://prefix.dev) for dependency management and project configuration. See the [Pixi installation guide](https://prefix.dev/docs/installation) for details.

Navigate into the main repository (e.g., `peasy`) and initialize a new Pixi project:

```bash
cd peasy
pixi init
```

### 2.3. Install Copier

Install Copier inside the Pixi environment:
```bash
pixi add copier
```

### 2.4 Generate Project Description (Home Repository)

> **Note:** This step generates only the project metadata, not code or structure.

```bash
pixi run copier copy gh:easyscience/templates .
```

Fill in the required information when prompted. For project name, alias, and short description, refer to the organization profile for consistency.

These answers are stored in a project description file `.project.yaml`, which becomes the single source of 
truth for all related repositories.

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

Now, set up Pixi and Copier for the library or application repository (e.g., `peasy-lib` or `peasy-app`):

```bash
cd peasy-lib
pixi init
pixi add copier
```

Apply both the Shared and Library-specific Copier templates to generate the project structure.

> **Important:** Use the `--data-file` option to provide the path to the `.project.yaml` file with answers created in the main repository (e.g., `peasy`).

```bash
pixi run copier copy gh:easyscience/templates-shared . --data-file ../peasy/.project.yaml
pixi run copier copy gh:easyscience/templates-lib . --data-file ../peasy/.project.yaml
```

When prompted with `conflict. overwrite pixi.toml?`, confirm with `Yes` to overwrite the Pixi configuration file created during `pixi init` with the one generated from the template.

After the project structure is generated, run the following commands to finalize the setup:

- **Install extra development dependencies and set up tools:**
  This step sets up pre-commit hooks, installs additional development dependencies, and configures non-Python file formatting.
  ```bash
  pixi run post-install
  ```

- **Update documentation assets:**
  Updates the logo and other assets in the `docs/` folder. Run this every time you update project-related logos or assets, especially after changes in the `easyscience/assets-branding` repository.
  ```bash
  pixi run docs-update-assets
  ```

- **Update SPDX license headers:**
  Updates license headers in all project files. Run this whenever the copyright year changes, new files are added, or license information needs to be refreshed.
  ```bash
  pixi run spdx-update
  ```

- **Format all project files:**
  Ensures all files adhere to the project's coding standards as defined in `pyproject.toml`. Run this after any changes to source code, configuration, workflows, or docs.
  ```bash
  pixi run fix
  ```

> **Tip:** Run `pixi run fix` every time after updating any template files or modifying any project files (source code, configuration, workflows, docs, etc.) to ensure consistent formatting.

### 2.6. Where Are Answers Stored?

The answers provided during setup are stored in:
- **Shared answers:** `peasy-lib/.copier-answers.shared.yml`
- **Project-specific answers:** `peasy-lib/.copier-answers.lib.yml`

They are autogenerated by Copier and should not be modified manually.

### 2.7. Push Changes to the Repository

After generating the project structure, **push the changes** to GitHub:
  ```bash
  git add -A
  git commit -m "Initial project setup using Copier shared and lib templates"
  git push origin master
  ```

### 2.8. Code Quality Checks

Templates set up pre-commit and pre-push hooks to ensure code quality. These hooks automatically check for code formatting, linting, and other quality standards before allowing commits or pushes.

If you see `commit failed` or `push failed` from pre-commit/pre-push hooks, fix the issues reported by those hooks, commit again, and push again.

To check issues reported by pre-commit hooks without committing, run:
```bash
pixi run pre-commit-check
```
or
```bash
pixi run pre-push-check
```

Often, running `pixi run fix` is enough to fix issues automatically. If not, follow the instructions provided in the output of the above commands to resolve all issues.

---




## 🛡️ Step 3: Post-Initialization Repository Setup

After you have made your initial commit and pushed to GitHub, complete the following steps:

### 3.1. Create develop Branch

Create and push the develop branch:
```bash
git checkout -b develop
git push -u origin develop
```

### 3.2. About gh-pages Branch and Pages Activation

The `gh-pages` branch will be created automatically by [mike](https://github.com/jimporter/mike) when you first deploy documentation. Do not attempt to activate GitHub Pages until this branch exists.

Once `gh-pages` exists, activate Pages deployment:
- Go to [GitHub Pages settings](https://github.com/easyscience/peasy-lib/settings/pages)
- In "Build and deployment" select **Source:** Deploy from a branch
- In **Branch** select `gh-pages` and click **Save**

> **Note:** Activating Pages deployment will add a workflow "pages build and deployment", which will be automatically triggered by `github-pages[bot]` after mike pushes a new version of docs to `gh-pages`.
>
> **Docs versioning:** Every new version of the documentation (built site) will be published under a dedicated directory named after the new release tag and added to the `gh-pages` branch. This allows users to access documentation for each release at a unique URL.

### 3.3. Set Repository Labels

Ensure correct labels, including the bot label ([see ADR](https://github.com/orgs/easyscience/discussions/33), [example](https://github.com/easyscience/peasy-lib/labels)).

### 3.4. Add Repository Secrets

Add repository secrets (e.g., API keys, deployment keys):
- The `easyscience[bot]` GitHub App should have access automatically (configured at the org level). Add it to the `develop` bypass protection rules for automatic backmerge after new releases.
- Add the PyPI API token secret for library repositories (for publishing to PyPI). Confirm if this is set at the org level.

### 3.5. Set Branch Protection Rules

Set branch protection rules ([GitHub Rules Settings](https://github.com/easyscience/peasy-lib/settings/rules)) only after the relevant branches exist:
- Create ruleset **"master branch protection"** with:
  - Enforcement status: Active
  - Branch targeting criteria: Add target → include default branch
  - Restrict deletions: ✔️
  - Require a pull request before merging: ✔️ (Allowed merge methods: Merge only)
  - Block force pushes: ✔️
  - Click "Save changes" button
- Create ruleset **"develop branch protection"** with:
  - Enforcement status: Active
  - Branch targeting criteria: Add target → include by pattern → develop
  - Restrict deletions: ✔️
  - Require a pull request before merging: ✔️ (Allowed merge methods: Squash only)
  - Block force pushes: ✔️
  - Click "Save changes" button
- Create ruleset **"gh-pages branch protection"** with:
  - Enforcement status: Active
  - Branch targeting criteria: Add target → include by pattern → gh-pages
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
2. Apply shared updates first (if any):
  ```bash
  pixi run copier-update-shared
  ```
  After completing commit your changes.
3. Apply project-specific updates (if any):
  ```bash
  pixi run copier-update-lib
  ```
  Commit again.

#### Using a Specific Version/Tag
To update to a specific version or tag of the templates (instead of the
default latest tagged release), specify the version in the Copier
command. This is useful for testing updates before official release:
```bash
pixi run copier-update-shared --vcs-ref=master
```

If conflicts arise, Copier will prompt you to review them.

Sometimes, for major template changes or complex conflicts, you may need to run Copier recopy instead of update:
```bash
pixi run copier-update-shared
# IMPORTANT: Do not forget to push your changes to GitHub before running the next command. If you do not push after copier-update-shared, copier-recopy-lib will not work due to a dirty repository state.
git add -A
git commit -m "Update after applying shared template"
git push origin master

pixi run copier-recopy-lib
# Push those changes to GitHub
git add -A
git commit -m "Update after applying project-specific template"
git push origin master
```


### GitHub Actions Workflows

Templates include a set of GitHub Actions workflows for CI/CD, testing, documentation building, and release management. Check the `.github/workflows/` directory for available workflows and their configurations.

## 🚀 Release Workflow

Follow these steps to create a new release and manage the release process:

1. Merge feature branches to develop as described in [ADR 12](https://github.com/orgs/easyscience/discussions/12).
2. To create an automated PR from develop to master for a new release, manually run the Release PR workflow from the Actions tab via the "Run workflow" button.
3. No need to manually set the package version. It is automatically suggested from PR labels (features → develop). Ensure correct PR labels and titles, as these are used to generate draft release notes.
4. After merging develop to master and creating a draft release, check that all release notes and the suggested tag/version are correct. Publish the release by clicking "Publish release". This triggers documentation site build, auto backmerge from tagged master to develop for version bumping, and PyPI publishing (for libraries).
