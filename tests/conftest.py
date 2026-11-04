# SPDX-FileCopyrightText: 2026 EasyScience contributors <https://github.com/easyscience>
# SPDX-License-Identifier: BSD-3-Clause
"""Render working template files without using a Git snapshot."""

import runpy
import shutil
import sys
from pathlib import Path

import pytest
from copier import run_copy

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def render_project(tmp_path):
    """Return a factory for rendering test projects."""
    source = tmp_path / 'source'
    source.mkdir()
    shutil.copy(ROOT / 'copier.yml', source)
    shutil.copytree(ROOT / 'template', source / 'template')

    def render(template_type='lib'):
        destination = tmp_path / template_type
        run_copy(
            str(source),
            str(destination),
            data={
                'project_name': 'EasyExample',
                'project_type': 'both',
                'template_type': template_type,
                'home_repo_name': 'example',
                'lib_repo_name': 'example-lib',
                'lib_package_name': 'easyexample',
                'app_repo_name': 'example-app',
                'app_package_name': 'easyexample_app',
            },
            defaults=True,
            quiet=True,
        )
        return destination

    return render


@pytest.fixture
def prepare_notebook(monkeypatch):
    """Run the generated preparation script."""

    def prepare(project, path):
        script = project / 'tools/prepare_notebooks_for_docs.py'
        monkeypatch.setattr(sys, 'argv', [str(script), str(path)])
        runpy.run_path(str(script), run_name='__main__')

    return prepare


@pytest.fixture
def finalize_notebooks(monkeypatch):
    """Run the generated after-build script on selected paths."""

    def finalize(project, *paths):
        script = project / 'tools/prepare_notebooks_for_colab.py'
        monkeypatch.setattr(sys, 'argv', [str(script), *(str(path) for path in paths)])
        runpy.run_path(str(script), run_name='__main__')

    return finalize
