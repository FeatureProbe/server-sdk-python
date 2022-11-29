import os
import sys

sys.path.insert(0, os.path.abspath(".."))


project = "featureprobe-server-sdk-python"
copyright = "FeatureProbe"
author = "FeatureProbe"
version = "1.x"


extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

source_suffix = ".rst"
master_doc = "index"

autodoc_member_order = "alphabetical"
