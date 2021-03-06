# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'introt'
copyright = '2021-2022, introt. Text is available under <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>'
author = 'introt'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autosectionlabel', 'sphinx.ext.todo']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabester'

html_sidebars = {
        # experimenting with the source link placements
        'raspberrypi/bluealsa': [
            'about.html',
            'sourcelink.html',
            'localtoc.html',
            'navigation.html',
            'searchbox.html',
        ],
        'index': [
            'about.html',
            'sourcelink.html',
            'searchbox.html',
        ],
        # Sphinx sets these for 'alabaster'; need to be set manually for forks
        '**': [
            'about.html',
            'navigation.html',
            #'relations.html',  # not shown anyway
            'sourcelink.html',  # extra
            'searchbox.html',
            #'donate.html'      # don't have one, wouldn't show up anyway
        ]
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_theme_options = {
        'description': 'stop-gaps for documentation gaps',
        'logo': 'logo.png',
        'logo_name': 'true',
        'logo_text_align': 'center',
}
