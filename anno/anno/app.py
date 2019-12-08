"""============================================================================
Configure and start local Anno notebook.
============================================================================"""

from   anno.anno.render import (jinja2_filter_date_to_string,
                                render_markdown,
                                make_pdf)
from   anno.anno.notes import build_notes
from   flask import (Flask,
                     send_from_directory,
                     redirect,
                     request,
                     render_template,
                     url_for)
import os


# -----------------------------------------------------------------------------

app = Flask(__name__)

app.jinja_env.filters['date_to_string'] = jinja2_filter_date_to_string
app.jinja_env.globals.update(zip=zip)


# -----------------------------------------------------------------------------

IMAGE_DIR = 'anno/static/images'
IMAGE_BASE_URL = '/static/images'
NOTES = build_notes()


# -----------------------------------------------------------------------------

@app.route('/', methods=['GET'])
def index():
    NOTES = build_notes()
    return render_template('index.html', notes=NOTES, title='Anno',
                           include_nav=False)


@app.route('/<string:note_title>', methods=['GET'])
def render_note(note_title):
    note = NOTES.get(note_title)
    return render_template('note.html', note=note,
                           text=render_markdown(note.text))


@app.route('/<string:note_url>/edit', methods=['GET', 'POST'])
def edit(note_url):
    note = NOTES.get(note_url)
    if request.method == 'GET':
        return render_template('edit.html', note=note,
                               rendered_text=render_markdown(note.text))
    else:
        new_text = request.form.get('note_text')
        note = NOTES.pop(note_url, None)
        if note:
            note.save(new_text)
            new_note_url = note.url
            # FIXME: Support rolling back.
            if new_note_url in NOTES:
                raise ValueError('')
            NOTES[new_note_url] = note
        return redirect(url_for('render_note', note_title=note.url))


@app.route('/preview', methods=['POST'])
def preview():
    text = request.form.get('note_text')
    return render_markdown(text)


@app.route('/<string:note_url>/delete', methods=['POST'])
def delete(note_url):
    note = NOTES.pop(note_url,  None)
    if note:
        note.trash()
    return redirect(url_for('index'))


@app.route('/<string:note_url>/archive', methods=['POST'])
def archive(note_url):
    note = NOTES.pop(note_url,  None)
    if note:
        note.archive()
    return redirect(url_for('index'))


@app.route('/label/<string:label>', methods=['GET'])
def label(label):
    filtered_notes = {u: n for u, n in NOTES.items() if label in n.labels}
    return render_template('index.html', notes=filtered_notes, title=label,
                           include_nav=True)


@app.route('/image', methods=['POST'])
def upload_image():
    f = request.files.get('file')
    fpath = os.path.join(IMAGE_DIR, f.filename)
    if os.path.exists(fpath):
        return 'Filename already exists. Please rename the image.'
    f.save(fpath)
    url = url_for('static', filename=f'images/{f.filename}')
    return f'<div class="image">' \
           f'    <img src="{url}" ' \
           f'        style="width: 100%%; display: block; margin: 0 auto;"/>' \
           f'    <p class="caption"></p>' \
           f'</div>'


@app.route('/<string:note_url>/pdf', methods=['GET'])
def pdf(note_url):
    note = NOTES.get(note_url,  None)
    make_pdf(note.text, note.pdf_fpath)
    return send_from_directory('', note.pdf_fname)
