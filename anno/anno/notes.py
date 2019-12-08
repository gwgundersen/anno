"""============================================================================
Configure and start local Anno web server.
============================================================================"""

import os
from   os import listdir
from   os.path import isfile, join
from   pathlib import Path
from   anno.anno.render import parse_metadata


ARCHIVE_DIR = '_archive'
NOTES_DIR   = '.'
STATIC_DIR  = 'static'
TRASH_DIR   = '_trash'


# -----------------------------------------------------------------------------

def standardize_word(word):
    """Standardize word in filename / URL.
    """
    return ''.join(e.lower() for e in word if e.isalnum())


def build_notes():
    notes = {}
    for f in listdir(NOTES_DIR):
        if isfile(join(NOTES_DIR, f)) and f.endswith('.md'):
            note = Note(join(NOTES_DIR, f))
            if note.url in notes:
                raise ValueError('two notes have the same date and title.')
            notes[note.url] = note
    return notes


# -----------------------------------------------------------------------------

class Note:

    def __init__(self, path):
        self.path = path
        with open(path) as f:
            text = f.read()
            meta = parse_metadata(text)
            self._update(meta)
        self.text = text

    def save(self, new_text):
        self.text = new_text
        with open(self.path, 'w') as f:
            f.write(new_text)
        meta = parse_metadata(new_text)
        self._update(meta)
        self.path = self.url

    def trash(self):
        if not os.path.exists(TRASH_DIR):
            os.makedirs(TRASH_DIR)
        self._move_to_dir(TRASH_DIR)

    def archive(self):
        if not os.path.exists(TRASH_DIR):
            os.makedirs(ARCHIVE_DIR)
        self._move_to_dir(ARCHIVE_DIR)

    def _move_to_dir(self, directory):
        fname = os.path.basename(self.path)
        os.rename(self.path, os.path.join(directory, fname))

    @property
    def pdf_fpath(self):
        return self.pdf_fname

    @property
    def pdf_fname(self):
        return str(Path(self.fname).with_suffix('.pdf'))

    def _update(self, meta):
        self.author = meta.get('author')
        self.date = meta.get('date')
        labels = meta.get('labels', '').split(',')
        if labels:
            labels = [l.strip() for l in labels]
        self.labels = labels
        self.subtitle = meta.get('subtitle')
        self.title = meta.get('title')

        parts = []
        for w in self.title.split(' '):
            sw = standardize_word(w)
            if sw != '':
                parts.append(sw)

        self.url   = '-'.join([self.date] + parts)
        self.fname = f'{self.url}.md'

        fpath = os.path.join(NOTES_DIR, self.fname)
        if fpath != self.path:
            # File on disk's name must match opinionated filename.
            os.rename(self.path, fpath)
            self.path = fpath
