# Contributing to EasyDynamics

We welcome contributions of all kinds: bug fixes, new features, documentation 
improvements, tests, and feedback.

Please make sure you follow our EasyScience organization-wide 
[Code of Conduct](https://github.com/easyscience/.github/blob/master/CODE_OF_CONDUCT.md) 
when participating in the project.

## Prerequisites

We use:

- **git** for version control  
- **GitHub** for repository hosting and CI/CD  
- **Pixi** for environment management and task execution  

Follow the official Pixi 
[installation instructions](https://pixi.prefix.dev/latest/installation/), 
as all EasyScience projects are configured to use Pixi for consistency and reproducibility.

See ADR `easyscience/.github#63` for the reasoning behind the choice of Pixi.

You should also have:

- A GitHub account  
- Basic familiarity with git commands  

---

## Development Process

Below is the recommended development workflow for contributing to this project.

---

### 1. If you are a first-time contributor

If you are contributing to this repository for the first time, follow these steps:

- Go to `easyscience/dynamics-lib` and click the **Fork** button to create your own copy of the project under your GitHub account.

- Clone your fork locally:

  ```bash
  git clone https://github.com/<your-username>/dynamics-lib.git
  ```

- Change into the project directory:

  ```bash
  cd dynamics-lib
  ```

- Add the original repository as `upstream`:

  ```bash
  git remote add upstream https://github.com/easyscience/dynamics-lib.git
  ```

- Fetch the latest changes and check out the `develop` branch.

  **Important:** We use the `develop` branch for ongoing development, not `master`.  
  More about our branching strategy can be found in ADR `easyscience/.github#12`.

  ```bash
  git fetch upstream
  git checkout develop
  git pull upstream develop
  ```

> If you have contributed before, make sure your local `develop` branch is up to date before creating a new feature branch.

---

### 2. Set up the development environment

- Create the default environment and install all declared dependencies:

  This installs all required dependencies, including testing and documentation tools.

  ```bash
  pixi install
  ```

- Install extra development dependencies and set up tools:

  This step installs additional development dependencies and configures formatting tools (including non-Python files):

  ```bash
  pixi run post-install
  ```

After this step, your local development environment should be fully configured.

---

### 3. Develop your contribution

- Create a new branch for the feature or fix you want to work on.  
  Since the branch name will appear in the merge message, use a sensible and descriptive name, for example `linspace-speedups`:

  ```bash
  git checkout -b linspace-speedups
  ```

- Commit locally as you progress:

  - Write clear and descriptive commit messages.  
  - Make frequent commits with logical chunks of work.

  ```bash
  git add .
  git commit -m "Improve performance of linspace for large arrays"
  ```

- Document any changed behavior in docstrings. Follow the Google docstring convention used in this project.

- Write unit tests that fail before your change and pass afterward.

  You can run tests locally with:

  ```bash
  pixi run unit-tests
  ```

---

### 4. Code Quality Checks

To ensure code quality, run:

```bash
pixi run check
```

This command runs:

- Formatting checks  
- Linting  
- Documentation format checks  
- Notebook format checks  
- Unit tests  
- Other project-specific validations  

The desired result should look similar to:

```bash
pixi run pyproject-check...................................Passed
pixi run py-lint-check.....................................Passed
pixi run py-format-check...................................Passed
pixi run nonpy-format-check................................Passed
pixi run docs-format-check.................................Passed
pixi run notebook-format-check.............................Passed
pixi run unit-tests........................................Passed
```

If any checks fail, read the error messages carefully and address the reported issues.

The full `pixi run check` command may take some time.  
At a minimum, always run it before opening a Pull Request.

You can execute individual checks separately, for example:

```bash
pixi run py-lint-check
```

Some checks may be automatically fixable (for example, formatting).  
In that case, run the relevant task to apply fixes:

```bash
pixi run fix
```

> **Tip:** After running `pixi run fix`, you should normally see the message  
> `✅ All code auto-formatting steps have been applied.`  
> This indicates that the full auto-formatting pipeline was executed successfully.
>
> If you do not see this message, try running the command again.
>
> Note that even if you see this message, there may still be issues that must be fixed manually.  
> Always review the command output carefully.

---

### 5. Documentation changes

Beyond updating code docstrings,  
if your change introduces any user-facing modifications, they must be reflected in the user documentation.

This may include:

- Updating API reference pages  
- Updating usage examples  
- Creating or updating Jupyter notebook tutorials  

After making documentation changes, build and preview them locally:

```bash
pixi run docs-serve
```

Then open the local server (usually shown in the terminal output) in your browser to verify that everything builds correctly and looks as expected.

---

### 6. Submitting your contribution

- Push your branch to your fork on GitHub:

  ```bash
  git push origin linspace-speedups
  ```

- Continuous Integration (CI) services are automatically triggered after each PR update.  
  They run tests, measure coverage, and check coding style.

If CI fails:

- Click on the red ❌ icon in GitHub  
- Inspect the logs  
- Fix the issues locally  
- Run `pixi run check`  
- Commit and push again  

To avoid unnecessary CI usage, always test locally before pushing.

- Go to GitHub. Your new branch will show a green **Compare & Pull Request** button.

When creating the PR:

- Make sure the title is clear and concise.  
- The PR title will be used as part of the release notes.  
- Each PR should preferably cover a single logical change.  

Make sure one of the required `[scope]` labels is assigned.

See ADR `easyscience/.github#33` about labels and version impact.

---

### 7. Review process

Reviewers (core developers and community members) will provide comments to help improve implementation, documentation, and style.

Every developer has their code reviewed.  
Code review is a collaborative and constructive process — it is meant to improve code quality, not to criticize contributors. We truly appreciate your time and effort.

To update your PR:

- Make changes locally  
- Commit them  
- Run checks again  
- Push to the same branch  

The PR updates automatically when you push.

If you are unsure how to fix something, you can:

- Push your partial changes  
- Ask questions directly in the PR discussion  

- CI checks must pass before the PR can be merged.  
- A PR must be approved by at least one core team member before merging.  

Approval means the changes have been reviewed and are ready to be integrated.

---

### 8. New Release

Once we release a new version (by merging `develop` into `master`),  
your work merged into the `develop` branch will propagate to the `master` branch and become part of a new stable release.

Thank you very much for your contribution!
