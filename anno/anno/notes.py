"""============================================================================
Configure and start local Anno web server.
============================================================================"""

import os
from   os import listdir
from   os.path import isfile, join
from   pathlib import Path
from   anno.anno.render import parse_metadata


FILE_EXT    = '.anno.md'
NOTES_DIR   = '.'
ARCHIVE_DIR = '_archive'
TRASH_DIR   = '_trash'
PDF_DIR     = '_pdf'


# -----------------------------------------------------------------------------

def get_notes(label=None):
    uids = set()
    notes = []
    for f in listdir(NOTES_DIR):
        if Note.is_note(f):
            note = Note.from_fname(f)
            if note.uid in uids:
                raise ValueError('two notes have the same date and title.')
            if label and label not in note.labels:
                continue
            uids.add(note.uid)
            notes.append(note)
    # Sorts in place.
    notes.sort(key=lambda x: x.date, reverse=True)
    return notes


def get_note(uid):
    for f in listdir(NOTES_DIR):
        if Note.is_note(f):
            note = Note.from_fname(f)
            if note.uid == uid:
                return note
    return None


def get_note_uids():
    uids = set()
    for f in listdir(NOTES_DIR):
        if Note.is_note(f):
            uid = Note.get_uid_from_fname(f)
            uids.add(uid)
    return uids


def note_exists(uid):
    return isinstance(get_note(uid), Note)


def standardize_word(word):
    """Standardize word in filename / URL.
    """
    return ''.join(e.lower() for e in word if e.isalnum())


def get_identifiers(title, date):
    parts = []
    for w in title.split(' '):
        sw = standardize_word(w)
        if sw != '':
            parts.append(sw)
    uid = '-'.join([date] + parts)
    fname = f'{uid}{FILE_EXT}'
    path = os.path.join(NOTES_DIR, fname)
    return path, fname, uid


def normalize_date(date):
    return date


def labels_str_to_list(labels):
    if labels:
        labels = labels.split(',')
        return [l.strip() for l in labels]
    return ''


# -----------------------------------------------------------------------------

class Note:

    def __init__(self, text):
        meta = parse_metadata(text)

        self.title = meta.get('title')
        self.date  = normalize_date(meta.get('date'))

        if self.title is None:
            raise AttributeError('a title must be given.')
        if self.date is None:
            raise AttributeError('a date must be given.')

        path, fname, uid = get_identifiers(self.title, self.date)

        self.text     = text
        self.path     = path
        self.fname    = fname
        self.uid      = uid
        self.labels   = labels_str_to_list(meta.get('labels'))
        self.subtitle = meta.get('subtitle')
        self.author   = meta.get('author')

    @property
    def url(self):
        return self.uid

    @property
    def pdf_fname(self):
        return str(Path(self.fname).with_suffix('.pdf'))

    @classmethod
    def is_note(cls, f):
        path = join(NOTES_DIR, f)
        return isfile(path) and f.endswith(FILE_EXT)

    @classmethod
    def from_fname(cls, fname):
        path = join(NOTES_DIR, fname)
        with open(path) as f:
            text = f.read()
        return cls(text)

    @classmethod
    def get_uid_from_fname(cls, fname):
        return fname.replace(FILE_EXT, '')

    def create_file(self):
        if os.path.exists(self.path):
            raise ValueError('File already exists.')
        with open(self.path, 'w') as f:
            f.write(self.text)

    def remove_file(self):
        os.remove(self.path)

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

