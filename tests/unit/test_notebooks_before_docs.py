# SPDX-FileCopyrightText: 2026 EasyScience contributors <https://github.com/easyscience>
# SPDX-License-Identifier: BSD-3-Clause
"""Check notebook preparation without changing authored cells."""

import subprocess  # noqa: S404
import sys
import tomllib

import nbformat


def test_prepare_notebooks(render_project, prepare_notebook):
    """Strip old output and add exactly one hidden setup cell."""
    project = render_project()
    manifest = tomllib.loads((project / 'pixi.toml').read_text())
    assert manifest['tasks']['notebook-prepare']['depends-on'] == [
        'notebook-strip',
        'notebook-prepare-docs',
    ]
    assert (
        'ipympl'
        in tomllib.loads((project / 'pyproject.toml').read_text())['project'][
            'optional-dependencies'
        ]['dev']
    )
    notebook_path = project / 'docs/docs/tutorials/tutorial.ipynb'
    notebook = nbformat.read(notebook_path, as_version=4)
    authored_sources = [cell.source for cell in notebook.cells]
    notebook.cells[-1].outputs = [nbformat.v4.new_output('stream', text='old output')]
    notebook.cells[-1].execution_count = 42
    notebook.metadata['widgets'] = {'old widget state': True}
    nbformat.write(notebook, notebook_path)
    # Isolate the CLI's stream handling from pytest's capture.
    subprocess.run(  # noqa: S603
        [sys.executable, '-m', 'nbstripout', str(notebook_path)], check=True
    )
    prepare_notebook(project, notebook_path.parent)
    prepared = nbformat.read(notebook_path, as_version=4)
    assert prepared.cells[0].metadata.tags == ['hide-in-docs', 'docs-static-plots']
    assert [cell.source for cell in prepared.cells[1:]] == authored_sources
    assert all(not cell.get('outputs') for cell in prepared.cells)
    assert all(cell.get('execution_count') is None for cell in prepared.cells)
    assert 'widgets' not in prepared.metadata
    first_result = notebook_path.read_bytes()
    prepare_notebook(project, notebook_path.parent)
    assert notebook_path.read_bytes() == first_result


def test_application_includes_notebook_setup(render_project):
    """Include notebook preparation in application projects too."""
    project = render_project('app')
    assert (project / 'tools/prepare_notebooks_for_docs.py').is_file()
    tasks = tomllib.loads((project / 'pixi.toml').read_text())['tasks']
    assert 'notebook-prepare-docs' in tasks
    assert 'notebook-prepare-docs' in tasks['notebook-prepare']['depends-on']
    assert (
        'ipympl'
        in tomllib.loads((project / 'pyproject.toml').read_text())['project'][
            'optional-dependencies'
        ]['dev']
    )
    after_script = project / 'tools/prepare_notebooks_for_colab.py'
    assert after_script.is_file()
    assert "PACKAGE_NAME = 'easyexample_app'" in after_script.read_text()
    assert 'prepare_notebooks_for_colab.py' not in (project / 'docs/mkdocs.yml').read_text()
