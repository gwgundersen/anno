"""============================================================================
Functions for rendering Markdown and LaTeX as HTML.
============================================================================"""

from   anno.anno.config import c
import datetime
import pypandoc
import re


# -----------------------------------------------------------------------------


def render_markdown(value):
    extra_args = ['--katex']
    output = pypandoc.convert_text(value,
                                   to='html5',
                                   format='md',
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


def jinja2_filter_date_to_string(date_str):
    date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    return date.strftime(c.datefmt)


# This function and regular expressions are taken from markdown2:
#
#     https://github.com/trentm/python-markdown2/blob/
#       4d2fc792abd7fbf8ddec937812857f13fded61cf/lib/markdown2.py#L453
#
# We aren't using this library because it's not clear from the docs how to just
# extract the metadata.
#
# -----------------------------------------------------------------------------

_meta_data_pattern = re.compile(
    r'^(?:---[\ \t]*\n)?'
    r'(.*:\s+>\n\s+[\S\s]+?)'
    r'(?=\n\w+\s*:\s*\w+\n|\Z)|([\S\w]+\s*:(?! >)'
    r'[ \t]*.*\n?)(?:---[\ \t]*\n)?',
    re.MULTILINE)
_key_val_pat = re.compile(r"[\S\w]+\s*:(?! >)[ \t]*.*\n?", re.MULTILINE)
# this allows key: >
#                   value
#                   continues over multiple lines
_key_val_block_pat = re.compile(
    "(.*:\s+>\n\s+[\S\s]+?)(?=\n\w+\s*:\s*\w+\n|\Z)", re.MULTILINE)
_meta_data_fence_pattern = re.compile(r'^---[\ \t]*\n', re.MULTILINE)
_meta_data_newline = re.compile("^\n", re.MULTILINE)


def _extract_metadata(text):

    # GWG: Sometimes extra `\r` characters are injected in the text. I am not
    #      sure why.
    text = text.replace('\r', '')

    metadata = {}
    if text.startswith("---"):
        fence_splits = re.split(_meta_data_fence_pattern, text,
                                maxsplit=2)
        metadata_content = fence_splits[1]
        match = re.findall(_meta_data_pattern, metadata_content)
        if not match:
            return text
    else:
        metadata_split = re.split(_meta_data_newline, text, maxsplit=1)
        metadata_content = metadata_split[0]
        match = re.findall(_meta_data_pattern, metadata_content)
        if not match:
            return text

    kv = re.findall(_key_val_pat, metadata_content)
    kvm = re.findall(_key_val_block_pat, metadata_content)
    kvm = [item.replace(": >\n", ":", 1) for item in kvm]

    for item in kv + kvm:
        k, v = item.split(":", 1)
        metadata[k.strip()] = v.strip()

    return metadata


def parse_frontmatter(text):
    try:
        metadata = _extract_metadata(text)
        return metadata
    except (ValueError, IndexError) as e:
        raise ValueError(f'Error parsing frontmatter: {str(e)}.')
