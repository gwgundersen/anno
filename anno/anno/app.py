"""============================================================================
Configure and start local Anno notebook.
============================================================================"""

from   anno.anno.config import c
from   anno.anno.render import (jinja2_filter_date_to_string,
                                render_markdown,
                                make_pdf)
from   anno.anno.notes import (get_notes,
                               get_note,
                               Note,
                               note_exists,
                               search_notes)
from   datetime import datetime
from   flask import (Flask,
                     flash,
                     jsonify,
                     make_response,
                     send_file,
                     redirect,
                     request,
                     render_template,
                     url_for)
import os
from   urllib.parse import unquote_plus

FNAME_WHITELIST = ['favicon.ico']


# -----------------------------------------------------------------------------
# Setup app.
# -----------------------------------------------------------------------------

app = Flask(__name__)
app.secret_key = 'This key is required for `flash()`.'
app.jinja_env.filters['date_to_string'] = jinja2_filter_date_to_string


# -----------------------------------------------------------------------------
# Routes.
# -----------------------------------------------------------------------------

@app.route('/', methods=['GET'])
def index():
    notes = get_notes()
    no_notes_msg = f'No notes in "{os.getcwd()}".'
    return render_template('index.html',
                           notes=notes,
                           title=c.notebook_title,
                           include_nav=False,
                           no_notes_msg=no_notes_msg)


@app.route('/<string:note_url>', methods=['GET'])
def render(note_url):
    note_uid = unquote_plus(note_url)
    note = get_note(note_uid)
    if not note or note_uid in FNAME_WHITELIST:
        flash(f'Note {note_uid} not found.')
        return redirect(url_for('index'))
    return render_template('note.html',
                           note=note,
                           highlight_css=c.highlight_css,
                           text=render_markdown(note.text))


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'GET':
        curr_date = datetime.now().strftime('%Y-%m-%d')
        default_text = """---
title: New note
date: %s
---""" % curr_date
        return render_template('new.html',
                               default_text=default_text)
    else:
        new_text = request.form.get('note_text')
        try:
            note = Note(new_text)
        except (ValueError, AttributeError) as e:
            flash(str(e))
            return render_template('new.html',
                                   default_text=new_text)
        if note_exists(note.uid):
            flash('New note has same date and title as another note.')
            return render_template('new.html', default_text=new_text)

        note.create_file()
        return redirect(url_for('render', note_url=note.url))


@app.route('/<string:note_url>/edit', methods=['GET', 'POST'])
def edit(note_url):
    note_uid = unquote_plus(note_url)
    if request.method == 'GET':
        note = get_note(note_uid)
        return render_template('edit.html',
                               note=note,
                               highlight_css=c.highlight_css)
    else:
        new_text = request.form.get('note_text')
        old_note = get_note(note_uid)
        try:
            new_note = Note(new_text)
        except (ValueError, AttributeError) as e:
            flash(str(e))
            old_note.text = new_text
            return render_template('edit.html',
                                   note=old_note,
                                   highlight_css=c.highlight_css)
        if new_note.uid != old_note.uid and note_exists(new_note.uid):
            flash('Modified note has same date and title as another note. '
                  'File was not created.')
            return render_template('edit.html',
                                   note=new_note,
                                   highlight_css=c.highlight_css)
        else:
            old_note.remove_file()
            new_note.create_file()
            return redirect(url_for('render', note_url=new_note.url))


@app.route('/<string:note_url>/save', methods=['POST'])
def save(note_url):
    note_uid = unquote_plus(note_url)
    new_text = request.form.get('note_text')
    old_note = get_note(note_uid)
    try:
        new_note = Note(new_text)
    except (ValueError, AttributeError) as e:
        print(str(e))
        return jsonify({
            'message': f'Not saved. {str(e)}',
            'success': False,
            'data': ''
        })
    if new_note.uid != old_note.uid and note_exists(new_note.uid):
        message = 'Not saved. Modified note has same date and title as ' \
                  'another note. File was not created.'
        return jsonify({
            'message': message,
            'success': False,
            'data': ''
        })
    else:
        old_note.remove_file()
        new_note.create_file()
        return jsonify({
            'message': 'File saved.',
            'success': True,
            'old_url': old_note.url,
            'new_url': new_note.url,
            'data'   : render_markdown(new_text)
        })


@app.route('/preview', methods=['POST'])
def preview():
    text = request.form.get('note_text')
    return render_markdown(text)


@app.route('/<string:note_url>/delete', methods=['POST'])
def delete(note_url):
    note_uid = unquote_plus(note_url)
    note = get_note(note_uid)
    if note:
        note.trash()
    return redirect(url_for('index'))


@app.route('/<string:note_url>/archive', methods=['POST'])
def archive(note_url):
    note_uid = unquote_plus(note_url)
    note = get_note(note_uid)
    if note:
        note.archive()
    return redirect(url_for('index'))


@app.route('/label/<string:label>', methods=['GET'])
def label(label):
    notes = get_notes(label=label)
    no_notes_msg = f'No notes for label "{label}".'
    return render_template('index.html', notes=notes, title=label,
                           show_home_btn=True, no_notes_msg=no_notes_msg)


@app.route('/image', methods=['POST'], defaults={'img_name': None})
@app.route('/image/<string:img_name>', methods=['GET'])
def image(img_name):
    IMAGE_DIR = os.path.join(os.getcwd(), c.image_dir)
    if request.method == 'GET':
        fpath = f'{IMAGE_DIR}/{img_name}'
        return send_file(fpath, mimetype='image/gif')
    else:
        f = request.files.get('file')
        if not os.path.exists(IMAGE_DIR):
            os.makedirs(IMAGE_DIR)
        fpath = os.path.join(IMAGE_DIR, f.filename)
        if os.path.exists(fpath):
            return 'Filename already exists. Please rename the image.'
        f.save(fpath)
        url = url_for('image', img_name=f.filename)
        return f'![caption]({url}){{ width=50% }}'


@app.route('/<string:note_url>/pdf', methods=['GET'])
def pdf(note_url):
    note_uid = unquote_plus(note_url)
    note = get_note(note_uid)

    try:
        make_pdf(note)
    except OSError:
        flash('Failed to convert to PDF. Is Pandoc installed?')
        return redirect(url_for('render', note_url=note_url))

    with open(note.pdf_fname, mode='rb') as f:
        response = make_response(f.read())
        response.headers['Content-Type'] = 'application/pdf'
        cd = f'inline; filename={note_uid}.pdf'
        response.headers['Content-Disposition'] = cd
    os.remove(note.pdf_fname)
    return response


@app.route('/search', methods=['POST'])
def search():
    keyword = request.form.get('search_text')
    notes   = search_notes(keyword)
    title   = f'search: "{keyword}"'
    no_notes_msg = 'No search results.'
    return render_template('index.html', notes=notes, title=title,
                           show_home_btn=True, include_nav=False,
                           no_notes_msg=no_notes_msg)
