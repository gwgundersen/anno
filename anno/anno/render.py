"""============================================================================
Functions for rendering Markdown and LaTeX as HTML.
============================================================================"""

import datetime
import pypandoc
import re


# -----------------------------------------------------------------------------

def render_markdown(value):
    output = pypandoc.convert_text(value, to='html5', format='md',
                                   extra_args=['--mathjax'])
    return output


def make_pdf(value, fname):
    extra_args = ['-V', 'geometry:margin=1in', '--pdf-engine', 'pdflatex']
    pypandoc.convert_text(value, to='pdf', format='md',
                          extra_args=extra_args,
                          outputfile=fname)


def parse_metadata(text):
    query = re.search(r'---\n(.*)\n---', text, re.DOTALL)
    # FIXME: Better markdown parsing.
    if not query:
        query = re.search(r'---\r\n(.*)\r\n---', text, re.DOTALL)
    if query:
        meta_raw = query.group(1)
        parts = meta_raw.split('\n')
        meta = {x[0].strip(): x[1].strip()
                for x in [x.split(':') for x in parts]}
        return meta
    return {}


def jinja2_filter_date_to_string(date_str):
    date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    return date.strftime('%d %B %Y')
