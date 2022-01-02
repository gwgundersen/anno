"""============================================================================
Configure and start local Anno web server.
============================================================================"""

from   anno.anno.render import parse_frontmatter
from   anno.anno.config import c
import datetime
import os
from   os import listdir
from   os.path import isfile, join
from   pathlib import Path
from   urllib.parse import quote_plus


NOTES_DIR = '.'


# -----------------------------------------------------------------------------
# Utility functions.
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


def get_identifiers(fm):
    uid   = c.gen_fname_base(fm)
    fname = Path(uid).with_suffix(c.extension)
    path  = os.path.join(NOTES_DIR, fname)
    return path, fname, uid


def normalize_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError(f'Incorrect date format {date_text}. Use YYYY-MM-DD.')
    return date_text


def labels_str_to_list(labels):
    if labels:
        labels = labels.split(',')
        return [l.strip() for l in labels]
    return ''


def search_notes(keyword):
    # FIXME: Is there a faster way to do this?
    notes = set()
    keyword = keyword.lower()
    for f in listdir(NOTES_DIR):
        if Note.is_note(f):
            note     = Note.from_fname(f)
            labels   = [l.lower() for l in note.labels]
            title    = note.title.lower()
            text     = note.text.lower()
            metavals = [v.lower() for k, v in note.meta.items()]
            if (keyword in labels
                    or keyword in title
                    or keyword in text
                    or keyword in metavals):
                notes.add(note)

    notes = list(notes)
    # Sorts in place.
    notes.sort(key=lambda x: x.date, reverse=True)
    return notes


# -----------------------------------------------------------------------------
# Note object.
# -----------------------------------------------------------------------------

class Note:

    def __init__(self, text, orig_fname=None):
        fm, _ = parse_frontmatter(text)

        self.title  = fm.get('title')
        self.author = fm.get('author')
        self.date   = fm.get('date')

        if self.title is None:
            raise AttributeError('A title must be given.')
        if self.date is None:
            raise AttributeError('A date must be given.')

        self.date = normalize_date(self.date)

        path, fname, uid = get_identifiers(fm)
        self.text   = text
        self.path   = path
        self.fname  = fname
        self.uid    = uid
        self.labels = labels_str_to_list(fm.get('labels'))

        # We treat/render the title, date, and author differently from other
        # metadata.
        self.meta = fm
        del self.meta['title']
        del self.meta['date']
        self.meta.pop('author', None)  # Safe delete.

        if orig_fname and orig_fname != fname:
            self.remove_file(orig_fname)
            self.create_file()

    @property
    def url(self):
        return quote_plus(self.uid)

    @property
    def pdf_fname(self):
        return str(Path(self.fname).with_suffix('.pdf'))

    @classmethod
    def from_fname(cls, fname):
        path = join(NOTES_DIR, fname)
        with open(path) as f:
            text = f.read()
        return cls(text, orig_fname=fname)

    @classmethod
    def is_note(cls, fname):
        path = join(NOTES_DIR, fname)
        return isfile(path) and fname.endswith(c.extension)

    @classmethod
    def get_uid_from_fname(cls, fname):
        return fname.replace(c.extension, '')

    def create_file(self):
        if os.path.exists(self.path):
            raise ValueError(f'File {self.path} already exists.')
        with open(self.path, 'w') as f:
            f.write(self.text)

    def remove_file(self, path=None):
        if path:
            os.remove(path)
        else:
            os.remove(self.path)

    def trash(self):
        if not os.path.exists(c.trash_dir):
            os.makedirs(c.trash_dir)
        self._move_to_dir(c.trash_dir)

    def archive(self):
        if not os.path.exists(c.archive_dir):
            os.makedirs(c.archive_dir)
        self._move_to_dir(c.archive_dir)

    def _move_to_dir(self, directory):
        fname = os.path.basename(self.path)
        os.rename(self.path, os.path.join(directory, fname))
