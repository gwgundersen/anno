"""============================================================================
Functions for rendering Markdown and LaTeX as HTML.
============================================================================"""

import datetime
import pypandoc
import re


# -----------------------------------------------------------------------------

def render_markdown(value):
    extra_args = ['--katex']
    output = pypandoc.convert_text(value, to='html5', format='md',
                                   extra_args=extra_args)
    return output


def make_pdf(note):
    extra_args = ['-V', 'geometry:margin=1in', '--pdf-engine', 'pdflatex']

    # FIXME. This is hacky. I'm replacing
    #   [my caption](/image/foo.png)
    # with
    #   [my caption](/_images/foo.png)
    # because I can't figure out how to tell Pandoc where the image files live.
    text = re.sub(r'(\(/image/)', '(_images/', note.text)

    pypandoc.convert_text(text, to='pdf', format='md',
                          extra_args=extra_args,
                          outputfile=note.pdf_fname)


def parse_frontmatter(text):
    if not text.startswith('---'):
        raise ValueError('Files must contain frontmatter with title and date.')
    try:
        # Credit: https://github.com/eyeseast/python-frontmatter/
        FM_BOUNDARY = re.compile(r'^-{3,}\s*$', re.MULTILINE)
        _, fm, content = FM_BOUNDARY.split(text, 2)
        parts = [p for p in fm.split('\n') if p]
        meta = {x[0].strip(): x[1].strip()
                for x in [x.split(':', 1) for x in parts]}
        return meta
    except ValueError:
        raise ValueError('Error parsing frontmatter.')


def jinja2_filter_date_to_string(date_str):
    date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    return date.strftime('%d %b %Y')
