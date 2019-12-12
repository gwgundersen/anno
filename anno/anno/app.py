"""============================================================================
Configure and start local Anno notebook.
============================================================================"""

from   anno.anno.render import (jinja2_filter_date_to_string,
                                render_markdown,
                                make_pdf)
from   anno.anno.notes import get_notes, get_note, Note, note_exists
from   datetime import datetime
from   flask import (Flask,
                     flash,
                     make_response,
                     send_file,
                     redirect,
                     request,
                     render_template,
                     url_for)
import os


# -----------------------------------------------------------------------------

app = Flask(__name__)
app.secret_key = 'This key is required for `flash()`.'

app.jinja_env.filters['date_to_string'] = jinja2_filter_date_to_string
app.jinja_env.globals.update(zip=zip)


# -----------------------------------------------------------------------------

@app.route('/', methods=['GET'])
def index():
    title = os.getcwd().split('/')[-1]
    notes = get_notes()
    return render_template('index.html', notes=notes, title=title,
                           include_nav=False, cwd=os.getcwd())


@app.route('/<string:note_uid>', methods=['GET'])
def render(note_uid):
    note = get_note(note_uid)
    return render_template('note.html', note=note,
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
        note = Note(new_text)
        if note_exists(note.uid):
            flash('New note has same date and title as another note.')
            return render_template('new.html', default_text=new_text)

        note.create_file()
        return redirect(url_for('render', note_uid=note.uid))


@app.route('/<string:note_uid>/edit', methods=['GET', 'POST'])
def edit(note_uid):
    if request.method == 'GET':
        note = get_note(note_uid)
        return render_template('edit.html', note=note,
                               rendered_text=render_markdown(note.text))
    else:
        new_text = request.form.get('note_text')
        old_note = get_note(note_uid)
        new_note = Note(new_text)
        if new_note.uid != old_note.uid and note_exists(new_note.uid):
            flash('Modified note has same date and title as another note.')
            return redirect(url_for('edit', note_uid=old_note.uid))
        else:
            old_note.remove_file()
            new_note.create_file()
            return redirect(url_for('render', note_uid=new_note.uid))


@app.route('/preview', methods=['POST'])
def preview():
    text = request.form.get('note_text')
    return render_markdown(text)


@app.route('/<string:note_uid>/delete', methods=['POST'])
def delete(note_uid):
    note = get_note(note_uid)
    if note:
        note.trash()
    return redirect(url_for('index'))


@app.route('/<string:note_uid>/archive', methods=['POST'])
def archive(note_uid):
    note = get_note(note_uid)
    if note:
        note.archive()
    return redirect(url_for('index'))


@app.route('/label/<string:label>', methods=['GET'])
def label(label):
    notes = get_notes(label=label)
    return render_template('index.html', notes=notes, title=label,
                           include_nav=True)


@app.route('/image', methods=['POST'], defaults={'img_name': None})
@app.route('/image/<string:img_name>', methods=['GET'])
def upload_image(img_name):
    IMAGE_DIR = os.path.join(os.getcwd(), '_images')
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
        url = url_for('upload_image', img_name=f.filename)
        return f'![caption]({url}){{ width=50% }}'


@app.route('/<string:note_uid>/pdf', methods=['GET'])
def pdf(note_uid):
    note = get_note(note_uid)
    make_pdf(note)
    with open(note.pdf_fname, mode='rb') as f:
        response = make_response(f.read())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % 'yourfilename'
    os.remove(note.pdf_fname)
    return response
