"""============================================================================
Functions for rendering Markdown and LaTeX as HTML.
============================================================================"""

import datetime
import os
import pypandoc
import re


# -----------------------------------------------------------------------------

def render_markdown(value):
    output = pypandoc.convert_text(value, to='html5', format='md',
                                   extra_args=['--mathjax'])
    return output


def make_pdf(note):
    extra_args = ['-V', 'geometry:margin=1in', '--pdf-engine', 'pdflatex']
    # FIXME. This is hacky. I'm replacing "(/image/" with "(_images/" in
    #
    #     [my caption](/image/foo.png)
    #
    # with
    #
    #     [my caption](foo.png)
    #
    # because I can't figure out how to tell Pandoc where the image file lives.
    text = re.sub(r'(\(/image/)', '(_images/', note.text)
    pypandoc.convert_text(text, to='pdf', format='md',
                          extra_args=extra_args,
                          outputfile=note.pdf_fname)


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
