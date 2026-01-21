# EasyScience Copier Templates

Welcome to the **EasyScience Copier Templates** repository! This project provides a robust, standardized approach for creating and maintaining repositories under the EasyScience organization. By leveraging [Copier](https://copier.readthedocs.io/), you can quickly scaffold new projects, ensure consistency, and streamline maintenance across all EasyScience projects.

---


## 📋 Table of Contents

1. [Quickstart Overview](#quickstart-overview)
2. [Introduction](#introduction)
3. [Available Templates](#available-templates)
4. [Step 1: Create New Repositories](#step-1-create-new-repositories)
5. [Step 2: Apply Templates and Initialize Projects](#step-2-apply-templates-and-initialize-projects)
  - [2.1. Clone All Repositories Locally](#21-clone-all-repositories-locally)
  - [2.2. Set Up Pixi](#22-set-up-pixi)
  - [2.3. Install Copier](#23-install-copier)
  - [2.4. Generate the Project Description File (Umbrella/Hub/Project Repository)](#24-generate-the-project-description-file-umbrellahubproject-repository)
  - [2.5. Generate the Project Structure (lib/app Repository)](#25-generate-the-project-structure-libapp-repository)
  - [2.6. Where Are Answers Stored?](#26-where-are-answers-stored)
  - [2.7. Push Changes to the Repository](#27-push-changes-to-the-repository)
  - [2.8. Code Quality Checks](#28-code-quality-checks)
6. [Step 3: Keep Your Repository Updated](#step-3-keep-your-repository-updated)
7. [FAQ & Troubleshooting](#faq--troubleshooting)
8. [Contributing](#contributing)
9. [License](#license)
## ⚡ Quickstart Overview

1. **Create repositories** for your umbrella/hub/project and any required lib/app repos on GitHub.
2. **Clone all repositories** locally.
3. **Initialize Pixi** in each repo for dependency management.
4. **Generate a project description file** in the umbrella/hub/project repo using Copier (no structure generated).
5. **Generate the project structure** in lib/app repos using Copier and the shared answers file.
6. **Push changes** to GitHub and follow code quality checks.
7. **Keep your repository updated** by applying template updates as needed.

---

## 📝 Introduction

This repository provides a structured approach to creating new repositories under the **EasyScience** organization using predefined templates. It ensures:
- Consistency across all projects
- Accelerated project setup
- Simplified maintenance and updates

---

## 🏗️ Available Templates

| Template  | Description | Source Repository |
|-----------|-------------|------------------|
| `shared`  | Shared base template with common files (LICENSE, CI workflows, etc.) | [easyscience/templates-shared](https://github.com/easyscience/templates-shared) |
| `lib`     | Python library template (e.g., diffraction-lib) | [easyscience/templates-lib](https://github.com/easyscience/templates-lib) |
| `app`     | Qt QML desktop application template (e.g., diffraction-app) | [easyscience/templates-app](https://github.com/easyscience/templates-app) |

---

## 🚀 Step 1: Create New Repositories

Depending on your project type (library, application, or both), you will need to create the corresponding repositories (e.g., `easyscience/peasy-lib`, `easyscience/peasy-app`), as well as the main umbrella/hub/project repository (e.g., `easyscience/peasy`).


### 1.1. Create and Set Up New Repositories

To create a new repository:

1. Go to [GitHub: Create New Repository](https://github.com/organizations/easyscience/repositories/new).
2. **Repository template:** Select "No template" (Copier templates will be used instead).
3. **Repository name:** Enter a name, e.g., `peasy`.
4. **Description:** Use the [EasyScience organization profile](https://github.com/easyscience/.github/blob/master/profile/README.md) for inspiration. If needed, update the org profile first.
5. **Visibility:** Set to **Public**.
6. **Do not initialize** with README, `.gitignore`, or license (Copier will handle these).
7. Click **Create repository**.
8. Repeat for additional repositories as needed:
   - For libraries: `peasy-lib`
   - For applications: `peasy-app`

### 1.2. Post-Creation and Manual Repository Configuration

After creating the repository, configure the following settings:
- **GitHub Pages:** Activate to serve documentation from the `gh-pages` branch.
- **Repository Labels:** Ensure correct labels, including the bot label ([see ADR](https://github.com/orgs/easyscience/discussions/33), [example](https://github.com/easyscience/peasy-lib/labels)).
- **Branch Protection Rules:**
  - Protect `master`, `develop`, and `gh-pages` branches.
  - Require pull request reviews and status checks before merging.
  - Include administrators in these rules.
- **Add repository secrets** (e.g., API keys, deployment keys):
  - The `easyscience[bot]` GitHub App should have access automatically (configured at the org level). Add it to the `develop` bypass protection rules for automatic backmerge after new releases.
  - Add the PyPI API token secret for library repositories (for publishing to PyPI). Confirm if this is set at the org level.

---




## 🛠️ Step 2: Apply Templates and Initialize Projects

### 2.1. Clone All Repositories Locally

```bash
git clone https://github.com/easyscience/peasy.git
git clone https://github.com/easyscience/peasy-lib.git
git clone https://github.com/easyscience/peasy-app.git
```

### 2.2. Set Up Pixi

We use [**Pixi**](https://prefix.dev) for dependency management and project configuration. See the [Pixi installation guide](https://prefix.dev/docs/installation) for details.

Navigate into the main umbrella/hub/project repository (e.g., `peasy`) and initialize a new Pixi project:

```bash
cd peasy
pixi init
```

### 2.3. Install Copier
```bash
pixi add copier
```

### 2.4. Generate the Project Description File (Umbrella/Hub/Project Repository)

> **Note:** This step generates only the project description file (answers file), not the project structure. This file will be reused as a data file with answers for other templates.

```bash
pixi run copier copy gh:easyscience/templates .
```

Fill in the required information when prompted. For project name, alias, and short description, refer to the organization profile for consistency.

This should create a `.project.yaml` file with all your answers. Push changes to GitHub:
```bash
git add -A
git commit -m "Initial project description file using Copier templates"
git push origin master
```

Navigate back to the parent directory:
```bash
cd ..
```

### 2.5. Generate the Project Structure (lib/app Repository)

Now, set up Pixi and Copier for the library or application repository (e.g., `peasy-lib` or `peasy-app`):

```bash
cd peasy-lib
pixi init
pixi add copier
```

Apply both the Shared and Library-specific Copier templates to generate the project structure.

> **Important:** Use the `--data-file` option to provide the path to the `.project.yaml` file with answers created in the main umbrella/hub/project repository (e.g., `peasy`).

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

### 2.7. Push Changes to the Repository

After generating the project structure, **push the changes** to GitHub. You can do this via:
- **Terminal:**
  Use your GitHub username and personal access token (PAT) as the password.
  ```bash
  git add -A
  git commit -m "Initial project setup using Copier shared and lib templates"
  git push origin master
  ```
- **GUI client:**
  Use a tool like GitKraken.

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


## 🔄 Step 3: Keep Your Repository Updated

When the templates in **templates-copier** are updated, apply those updates to your project.


### 📌 To update the repository with template changes:

1. Go to the project directory, e.g., `peasy-lib`:
  ```bash
  cd peasy-lib
  ```
2. **Update the Common Template:**
  ```bash
  pixi run copier-update-shared
  ```
  Push those changes to GitHub.
3. **Update the Project-Specific Template:**
  ```bash
  pixi run copier-update-lib
  ```
  Push those changes to GitHub.

#### Using a Specific Version/Tag
To update to a specific version or tag of the templates (instead of the latest tagged release), specify the version in the Copier command. This is useful for testing updates before official release:
```bash
pixi run copier-update-shared --vcs-ref=master
```

If conflicts arise, Copier will prompt you to review them.

Sometimes, for major template changes or complex conflicts, you may need to run Copier recopy instead of update:
```bash
pixi run copier-update-shared
# Push those changes to GitHub

pixi run copier-recopy-lib
# Push those changes to GitHub
```


### GitHub Actions Workflows

Templates include a set of GitHub Actions workflows for CI/CD, testing, documentation building, and release management. Check the `.github/workflows/` directory for available workflows and their configurations.


> **Note:**
> - Merge feature branches to develop as described in [ADR 12](https://github.com/orgs/easyscience/discussions/12).
> - To create an automated PR from develop to master for a new release, manually run the Release PR workflow from the Actions tab via the "Run workflow" button.
> - No need to manually set the package version. It is automatically suggested from PR labels (features → develop). Ensure correct PR labels and titles, as these are used to generate draft release notes.
> - After merging develop to master and creating a draft release, check that all release notes and the suggested tag/version are correct. Publish the release by clicking "Publish release". This triggers documentation site build, auto backmerge from tagged master to develop for version bumping, and PyPI publishing (for libraries).

---

## ❓ FAQ & Troubleshooting

**Q: Why isn't my answers file being generated?**
A: Ensure you are running Copier in the umbrella/hub/project repository and that the template includes a file for the answers file (e.g., `.project.yaml.jinja`).

**Q: Copier prompts to overwrite `pixi.toml`. Should I say yes?**
A: Yes, confirm with `Yes` to use the template's configuration.

**Q: How do I update templates after my project is created?**
A: See [Step 3: Keep Your Repository Updated](#step-3-keep-your-repository-updated).

**Q: Where are my answers stored?**
A: See [2.6. Where Are Answers Stored?](#26-where-are-answers-stored).

**Q: What if pre-commit or pre-push hooks fail?**
A: Run `pixi run fix` and follow the instructions in the error output.

If you encounter other issues, please open an issue or discussion in this repository.
