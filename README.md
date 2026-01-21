# Copier Templates

This repository provides a structured approach to creating new repositories under the 
**EasyScience** organization using predefined templates. It ensures consistency, accelerates 
project setup and simplifies maintenance across multiple projects.

## Available Templates

- `shared` – Shared base template with common files (LICENSE, CI workflows, etc.). Source code is in the separate
  repository [easyscience/templates-shared](https://github.com/easyscience/templates-shared).
- `lib` - Python library template (e.g., diffraction-lib). Source code is in the separate repository 
  [easyscience/templates-lib](https://github.com/easyscience/templates-lib).
- `app` - Qt QML desktop application template (e.g., diffraction-app). Source code is in the separate repository 
  [easyscience/templates-app](https://github.com/easyscience/templates-app).

## 🚀 Step 1: Create New Repositories

Depends on the type of the project (library, application or both) you need to create the corresponding
repositories (e.g. easyscience/peasy-lib and/or easyscience/peasy-app), as well as the main umbrella/hub/project
repository (e.g. easyscience/peasy).

### 1.1. Create a Repository on GitHub

To create a new repository, follow these steps:

- Navigate to **GitHub** and click **"Create New Repository"** 
  (https://github.com/organizations/easyscience/repositories/new).
- Repository template: No template (as we will use Copier templates instead of GitHub templates).
- Enter the repository name, for example, `peasy`.
- Add a description based on the 
  [EasyScience organization profile](https://github.com/easyscience/.github/blob/master/profile/README.md). 
  If a suitable description isn't available, consider adding one to the organization profile first.
- Set the repository visibility to **Public**.
- Ensure **not to initialize** the repository with a README, `.gitignore`, or license file, as these will be handled by Copier.
- Click **"Create repository"** to finalize the process.
- Repeat the above steps for creating additional repositories as needed:
  - For library projects, create a `peasy-lib` repository.
  - For application projects, create a `peasy-app` repository.

After creating the repository, make sure to configure the following settings:
- Activate GitHub Pages to serve documentation from the `gh-pages` branch.
- Make sure you have a correct set of repo labels including bot label (see ADR https://github.com/orgs/easyscience/discussions/33 and a 
  example project  https://github.com/easyscience/peasy-lib/labels)
- **Branch Protection Rules**:
  - Protect the `master` branch:
    - Require pull request reviews before merging.
    - Require status checks to pass before merging.
    - Include administrators in these rules.
  - Protect the `develop` branch similarly to `master`.
  - Protect the `gh-pages` branch ...


## ⚙️ Step 2: Perform Manual Repository Configuration
Some repository settings might need manual adjustment:
- **Add repository secrets** (e.g., API keys, deployment keys).
  - `easyscience[bot]` GitHub App should have access automatically, as it is configured 
    at the organization level. Do not forget to add it to the `develop` bypass
    protection rules as well (for automatic backmerge to develop after new release).
  - PyPI API token secret for library repositories (for publishing to PyPI). Is it als on 
    org level???




#### Clone all those repositories locally and set them up with Copier templates

```bash
git clone https://github.com/easyscience/peasy.git
git clone https://github.com/easyscience/peasy-lib.git
git clone https://github.com/easyscience/peasy-app.git
```

#### Create the project description file via Copier in the main umbrella/hub/project repository
to be used as a source of answers for all other repositories.

### 1.3. Set up Pixi

To set up and maintain EasyScience projects we are using
[**Pixi**](https://prefix.dev), a modern package manager for Windows,
macOS, and Linux that simplifies dependency management and project configuration.

See the official [Pixi installation guide](https://prefix.dev/docs/installation)
for detailed instructions.

Now, navigate into the main umbrella/hub/project repository (e.g., `peasy`) and initialize a new Pixi project:
```bash
cd peasy
pixi init
```

In the terminal-based approach, this can be done with:
```bash
git clone https://github.com/easyscience/peasy-lib.git
cd peasy-lib
```

### 1.4. Generate the Project Structure Using Copier

#### 🛠 Install Copier
```bash
pixi add copier
```

#### 📂 Create the Initial Repository Structure
Apply the Copier templates to generate the project structure. 

```bash
pixi run copier copy gh:easyscience/templates .
```

Fill in the required information when prompted. For project name, alias and short description,
you can refer to the organization profile for consistency....

This should create `.project.yaml` file with all those answers. Push changes to GitHub.
```bash
git add -A
git commit -m "Initial project setup using Copier templates"
git push origin master
```

Now, navigate back to the parent directory:
```bash
cd ..
```

Now, let's set up Pixi and Copier for the library repository (e.g., `peasy-lib`):

```bash
cd peasy-lib
pixi init
pixi add copier
```

Apply both the Shared and Library-specific Copier templates to generate the project structure. 
!!! Important: Use the `--data-file` option to provide the path to the 
`.project.yaml` file with answers created in the main umbrella/hub/project repository (e.g., 
`peasy`).

```bash
pixi run copier copy gh:easyscience/templates-shared . --data-file ../peasy/.project.yaml
pixi run copier copy gh:easyscience/templates-lib . --data-file ../peasy/.project.yaml
```

Fill in the required information when prompted. When seeing 
`conflict. overwrite pixi.toml?`, confirm with `Yes`, as this is needed to
overwrite the Pixi configuration file created temporarily during `pixi init` with the one 
generated from the template.


After the project structure is generated, run the following commands to finalize the setup.

First, perform post-installation tasks required for extra development dependencies and 
configurations, like setting up pre-commit hooks, non-python file formatting, etc.

```bash
pixi run post-install
```

Once the post-installation is complete, run the code formatter to ensure all files
adhere to the project's coding standards (defined in the pyproject.toml file):

```bash
pixi run fix
```

Important, the above command should be run every time after updating any template files or 
modifying any project files (source code, configuration, workflows, docs, etc.) to ensure 
consistent formatting.

For a correct build of the documentation site after updating the templates,
make sure to run:
```bash
pixi run docs-update-assets
```
which updates the logo assets in the `docs/` folder. Dot it every time after updating
the project related logos, etc. at `easyscience/assets-branding` repository.

For SPDX license updates, make sure to run:
```bash
pixi run spdx-update
pixi run fix # Needed to reformat files after license header update
```
whenever the licence header in any of the project files needs to be updated
because of the copyright year change, new files added, etc.


#### 🔍 Code Quality Checks
Templates also set up pre-commit and pre-push hooks to ensure code quality.
These hooks automatically check for code formatting, linting, and other quality
standards before allowing commits or pushes.

If you see `commit failed` or `push failed` from pre-commit/pre-push hooks,
make sure to fix the issues reported by those hooks, commit again, and push again.

To check issues reported by pre-commit hooks without committing, run:
```bash
pixi run pre-commit-check
```
or
```bash
pixi run pre-push-check
```

Often, running `pixi run fix` is enough to fix the issues automatically. If not,
follow the instructions provided in the output of the above commands in order to fix
all issues.



#### 📁 Where Are Answers Stored?
The answers provided during setup are stored in:
- **Shared answers** → `peasy-lib/.copier-answers.shared.yml`
- **Project-specific answers** → `peasy-lib/.copier-answers.lib.yml`


### 1.5. Push Changes to the Repository
After generating the project structure, **push the changes** to GitHub. You can do this via:
- The **terminal**:
  Use your username for 'https://github.com' along with the personal access token (PAT) as the password.
  ```bash
  git add -A
  git commit -m "Initial project setup using Copier shared and lib templates"
  git push origin master
  ```
- A **GUI client** like GitKraken.



## 🔄 Step 3: Keep Your Repository Updated with Template Changes
When the templates in **templates-copier** are updated, apply those updates to your project.

### 📌 To update the repository with the template changes:

Go to the project directory, e.g., `peasy-lib`:
```bash
cd peasy-lib
```

Step 1: Update the Common Template
```bash
pixi run copier-update-shared
```
Now push those changes to GitHub

Step 2: Update the Project-Specific Template, e.g. for `lib` template
```bash
pixi run copier-update-lib
```
Now push those changes to GitHub

### Using a specific version/tag
To update to a specific version or tag of the templates, instead of the latest tagged release,
you can specify the version in the Copier command. This is useful if you want to
test updates before they are officially released.
For example:
```bash
pixi run copier-update-shared --vcs-ref=master
```


- If conflicts arise, Copier will prompt you to review them.

Sometimes, in case of major template changes, and conflicts are too complex,
you might need to run Copier recopy again instead of update. This can be done via:
```bash
pixi run copier-update-shared
# Now push those changes to GitHub

pixi run copier-recopy-lib
# Now push those changes to GitHub
```

### Workflows

Templates have a set of GitHub Actions workflows for CI/CD, testing, documentation building,
and release management. Make sure to check the `.github/workflows/` directory for available workflows
and their configurations.

!!! Merge feature branches to develop as described in ADR https://github.com/orgs/easyscience/discussions/12

!!! To create an automated PR from develop to master for a new release,
manually run Release PR workflow from Actions tab via "Run workflow" button.

!!! No need to manually set package version. It should be automatically suggested from PR 
labels (fratures -> develop), so take care of correct PR labels and titles, which are used
to generate draft release notes as well.

!!! When draft release is created (after merging develop to master), check that all
release notes are correct and the suggested tag/version is correct. Then publish the release by 
clicking "Publish release" button. This will trigger building documentation site as well, 
auto backmerge from tagged master to develop for proper version bumping in develop, and 
PyPI publishing (library only).



## 🎯 Summary
| **Step** | **Description** |
|---------|----------------|
| **Step 1** | Create a repository and initialize it using Copier templates. |
| **Step 2** | Perform manual configuration for repository settings. |
| **Step 3** | Keep the repository updated with the latest template changes using `copier update`. |
