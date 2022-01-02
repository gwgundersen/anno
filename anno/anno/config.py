"""============================================================================
Configuration handling.
============================================================================"""

import importlib.util
import os
from   pathlib import Path


# Location of user-generated config file.
CPATH = Path(os.getcwd(), '.anno_config.py')


# -----------------------------------------------------------------------------
# Utility functions.
# -----------------------------------------------------------------------------

def standardize_title(title):
    """Standarize title.
    """
    parts = []
    for w in title.split(' '):
        sw = ''.join(e.lower() for e in w if e.isalnum())
        if sw != '':
            parts.append(sw)
    return '-'.join(parts)


def generate_config():
    """Generate user configuration file if it does not exist. Raise ValueError
    if it already exists.
    """
    default_user_config_content = '''# Configuration file for Anno notebook.
# =====================================

c = {}

# # Set which file extension is used.
# c['extension'] = '.anno.md'

# # Set notebook title displayed on index page.
# c['notebook_title'] = 'Notes'

# # Set the archive, image, and trash directories.
# c['archive_dir'] = '_archive'
# c['image_dir'] = '_images'
# c['trash_dir'] = '_trash'

# # The date format use when rendering dates.
# c['datefmt'] = '%d %b %Y'

# # Specify how filenames are generated.
# def gen_fname_base(fm):
#     """`fm` is a dictionary of key-value pairs representing data in the
#     notes' frontmatter.
#     """
#     return f"{fm['date']}-{fm['title']}"
# c['gen_fname_base'] = gen_fname_base

# # Specify how code style. For examples, see:
# # https://www.garrickadenbuie.com/blog/pandoc-syntax-highlighting-examples/
# # Options:
# # - highlight-default.css
# # - highlight-espressor.css
# # - highlight-haddock.css
# # - highlight-kate.css
# # - highlight-monochrome.css
# # - highlight-pygments.css
# # - highlight-tango.css
#
# c['highlight_css'] = 'highlight-kate.css'
'''
    if CPATH.exists():
        msg = f'User-generated config file already exists at: {CPATH}. ' \
              f'To reset the user config, please remove this file first.'
        raise ValueError(msg)
    else:
        with open(CPATH, 'w+') as f:
            f.write(default_user_config_content)
        return CPATH


def merge_configs():
    """Merge default and user-generated configs, stepping on former with values
    from the latter.
    """
    c = Config()
    if CPATH.exists():
        spec = importlib.util.spec_from_file_location('configfile', CPATH)
        user_config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_config)

        # Overwrite defaults with any matching user config.
        for key, val in user_config.c.items():
            if getattr(c, key):
                setattr(c, key, val)
            else:
                msg = f'Option "{key}" is not configurable.'
                raise ValueError(msg)
    return c


# -----------------------------------------------------------------------------
# Configuration object for easy dot access.
# -----------------------------------------------------------------------------

class Config:

    def __init__(self):
        self.archive_dir    = '_archive'
        self.image_dir      = '_images'
        self.trash_dir      = '_trash'
        self.datefmt        = '%d %b %Y'
        self.extension      = '.anno.md'
        self.notebook_title = os.getcwd().split('/')[-1]
        self.highlight_css  = 'highlight-kate.css'

    def gen_fname_base(self, fm):
        date   = fm['date']
        title  = fm['title']
        stitle = standardize_title(title)
        uid    = f'{date}-{stitle}'
        return uid


# -----------------------------------------------------------------------------
# Construct globally accessible, merged config.
# -----------------------------------------------------------------------------

c = merge_configs()
