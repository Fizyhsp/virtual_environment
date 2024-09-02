"""Spinx configuration."""  # noqa: INP001
import sys
from datetime import datetime
from os import chdir
from pathlib import Path

import alabaster

sys.path.insert(
    0,
    Path(__file__).parents[2].as_posix(),
)
chdir(Path(__file__).parents[2].as_posix())
author = "1746104160 Linkseed49 Fizyhsp luol517 hqh312 chacha447"
release = "0.2.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "alabaster",
    "sphinx_issues",
    "autodocsumm",
]

primary_domain = "py"
default_role = "py:obj"

intersphinx_mapping = {
    "python": ("https://python.readthedocs.io/en/latest/", None),
}


issues_github_path = "1746104160/lawen"

templates_path = ["_templates"]


# Use SOURCE_DATE_EPOCH for reproducible build output https://reproducible-builds.org/docs/source-date-epoch/
build_date = datetime.now()  # noqa: DTZ005

source_suffix = ".rst"
master_doc = "index"

project = "lawen"
copyright = (  # noqa: A001
    f" {build_date:%Y} 1746104160 Linkseed49 Fizyhsp luol517 hqh312 chacha447"
)
version = release = "0.2.0"
exclude_patterns = ["_build"]

language = "zh_CN"

# THEME

html_theme_path = [alabaster.get_path()]
html_theme = "alabaster"
html_static_path = ["_static"]
html_css_files = ["css/versionwarning.css"]
templates_path = ["_templates"]
html_show_sourcelink = False

html_theme_options = {
    "logo": "lawen.png",
    "description": "Large Language Model Agent for Web Environment",
    "description_font_style": "italic",
    "github_user": "1746104160",
    "github_repo": "lawen",
    "github_banner": True,
    "github_type": "star",
    "opencollective": "1746104160",
    "code_font_size": "0.8em",
    "warn_bg": "#FFC",
    "warn_border": "#EEE",
    # Used to populate the useful-links.html template
    "extra_nav_links": {
        "lawen @ PyPI": "https://pypi.python.org/pypi/lawen",
        "lawen @ GitHub": "https://github.com/1746104160/lawen",
        "Issue Tracker": "https://github.com/1746104160/lawen/issues",
    },
}

html_sidebars = {
    "index": [
        "about.html",
        "searchbox.html",
        "useful-links.html",
    ],
    "**": [
        "about.html",
        "searchbox.html",
        "useful-links.html",
        "localtoc.html",
        "relations.html",
    ],
}

# Show warning at top of page
versionwarning_body_selector = "div.document"
versionwarning_banner_title = ""
# For debugging locally
