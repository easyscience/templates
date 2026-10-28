# SPDX-FileCopyrightText: 2026 EasyScience contributors <https://github.com/easyscience>
# SPDX-License-Identifier: BSD-3-Clause
"""Check published notebooks, HTML, and notebook action links."""

import importlib.util
import shutil

import nbformat
import pytest
import yaml
from mkdocs.commands.build import build
from mkdocs.config import load_config


def load_script(project):
    """Import the generated after-build script."""
    spec = importlib.util.spec_from_file_location(
        'notebook_finalize', project / 'tools/prepare_notebooks_for_colab.py'
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(
    ('installed', 'expected'),
    [
        ('0.8.0', 'easyexample==0.8.0'),
        ('0.8.0rc1', 'easyexample==0.8.0rc1'),
        ('0.8.0.dev1', 'easyexample'),
        ('0.8.0+devdirty1', 'easyexample'),
        ('999.0.0', 'easyexample'),
    ],
)
def test_package_version(render_project, monkeypatch, installed, expected):
    """Choose an installable package specifier for each build type."""
    script = load_script(render_project())
    monkeypatch.setattr(script, 'version', lambda _: installed)
    assert script.pip_specifier() == expected


@pytest.mark.parametrize('directory_urls', [False, True])
def test_published_notebook(render_project, prepare_notebook, finalize_notebooks, directory_urls):
    """Replace only our cell after rendering, for either URL layout."""
    project = render_project()
    docs = project / 'docs'
    config_path = docs / 'check.yml'
    (docs / 'check_docs/tutorials/nested').mkdir(parents=True)
    notebook_path = docs / 'check_docs/tutorials/nested/example.ipynb'
    output = nbformat.v4.new_output('stream', text='Preserved example output\n')
    authored = nbformat.v4.new_code_cell(
        "print('Preserved example output')",
        metadata={'tags': ['hide-in-docs', 'authored-cell']},
        outputs=[output],
        execution_count=1,
    )
    widgets = {
        'application/vnd.jupyter.widget-state+json': {
            'version_major': 2,
            'version_minor': 0,
            'state': {},
        }
    }
    notebook = nbformat.v4.new_notebook(cells=[authored], metadata={'widgets': widgets})
    nbformat.write(notebook, notebook_path)
    prepare_notebook(project, notebook_path)
    original = notebook_path.read_bytes()
    # Use the generated override with a small test site, without hooks.
    shutil.copytree(docs / 'overrides', docs / 'check_overrides')
    config_path.write_text(
        yaml.safe_dump({
            'site_name': 'Notebook check',
            'site_url': 'https://easyscience.github.io/example-lib/dev/',
            'docs_dir': 'check_docs',
            'site_dir': 'check_site',
            'use_directory_urls': directory_urls,
            'theme': {'name': 'material', 'custom_dir': 'check_overrides'},
            'extra': {
                'vars': {'github_repository': 'easyscience/example-lib', 'docs_version': 'dev'}
            },
            'plugins': [
                {
                    'mkdocs-jupyter': {
                        'execute': False,
                        'include_source': True,
                        'remove_tag_config': {'remove_input_tags': ['hide-in-docs']},
                    }
                }
            ],
        }),
        encoding='utf-8',
    )
    config = load_config(str(config_path))
    build(config)
    relative_dir = 'tutorials/nested/example' if directory_urls else 'tutorials/nested'
    site_dir = docs / 'check_site'
    published_path = site_dir / relative_dir / 'example.ipynb'
    html_path = site_dir / relative_dir / ('index.html' if directory_urls else 'example.html')
    html = html_path.read_text()
    assert 'Preserved example output' in html
    assert 'snapshot_canvases' not in html
    assert '%pip install' not in html
    assert (
        'https://colab.research.google.com/github/easyscience/example-lib/blob/gh-pages/dev/'
        f'{relative_dir}/example.ipynb'
    ) in html
    assert notebook_path.read_bytes() == original
    assert nbformat.read(published_path, as_version=4).cells[0].metadata.tags == [
        'hide-in-docs',
        'docs-static-plots',
    ]
    finalize_notebooks(project, site_dir, notebook_path.parent)
    published = nbformat.read(published_path, as_version=4)
    assert len(published.cells) == 2
    assert published.cells[0].metadata.tags == ['hide-in-docs', 'colab-install']
    assert '%pip install easyexample' in published.cells[0].source
    assert published.cells[1] == authored
    assert published.metadata.widgets == widgets
    assert nbformat.read(notebook_path, as_version=4) == published
    assert 'docs-static-plots' not in published_path.read_text()
    first_result = published_path.read_bytes()
    finalize_notebooks(project, site_dir, notebook_path.parent)
    assert published_path.read_bytes() == first_result
    assert html_path.read_text() == html
    # Mike rebuilds from finalized copies, with the installer hidden.
    build(config)
    assert published_path.read_bytes() == first_result
    assert notebook_path.read_bytes() == first_result
    rebuilt_html = html_path.read_text()
    assert 'Preserved example output' in rebuilt_html
    assert '%pip install' not in rebuilt_html
    assert 'snapshot_canvases' not in rebuilt_html


@pytest.mark.parametrize('template_type', ['lib', 'app'])
def test_ci_notebook_step_order(render_project, template_type):
    """Make both scripts explicit in the CI build sequence."""
    project = render_project(template_type)
    workflow = yaml.safe_load((project / '.github/workflows/docs.yml').read_text())
    steps = workflow['jobs']['build-deploy-docs']['steps']
    names = [step['name'] for step in steps]
    expected = [
        'Build site for local check',
        'Prepare notebooks for download and Colab',
        'Upload built site as artifact',
        'Rebuild and deploy docs with mike',
    ]
    if template_type == 'lib':
        expected = [
            'Strip notebook outputs',
            'Add static plot setup to notebooks',
            'Run notebooks',
            *expected,
        ]
    assert [names.index(name) for name in expected] == sorted(
        names.index(name) for name in expected
    )
    assert 'hooks:' not in (project / 'docs/mkdocs.yml').read_text()
