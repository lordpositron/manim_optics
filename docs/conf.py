"""Sphinx configuration for manim-optics documentation."""

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

# -- Project info -------------------------------------------------------------
project = "manim-optics"
author = "Corentin Nannini"
copyright = "2024, Corentin Nannini"
release = "0.1.0"
version = "0.1.0"

# -- General configuration ----------------------------------------------------
extensions = [
    "autoapi.extension",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# MyST settings
myst_enable_extensions = ["colon_fence", "deflist"]
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# -- AutoAPI ------------------------------------------------------------------
# Analyses source code statically (AST) — no import needed, manim not required.
autoapi_dirs = ["../manim_optics"]
autoapi_type = "python"
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "special-members",
    "imported-members",
]
autoapi_member_order = "bysource"
autoapi_add_toctree_entry = True
autoapi_keep_files = True

# -- Napoleon (NumPy/Google docstrings) ---------------------------------------
napoleon_numpy_docstring = True
napoleon_google_docstring = False
napoleon_include_init_with_doc = True

# -- Intersphinx --------------------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
}

# -- HTML output --------------------------------------------------------------
html_theme = "furo"
html_title = "manim-optics"
html_static_path = ["_static"]
html_logo = "../manim-optics-logo.svg"
html_theme_options = {
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "source_repository": "https://github.com/lordpositron/manim_optics",
    "source_branch": "main",
    "source_directory": "docs/",
}
pygments_style = "friendly"
pygments_dark_style = "monokai"
