"""A Flask-based Anno notebook server.
"""

from   anno.anno.app import app
import webbrowser


def main():
    # FIXME: These should be configurable.
    PORT = 5000
    webbrowser.open_new_tab(f'http://localhost:{PORT}/')
    app.run(debug=True,
            host='0.0.0.0',
            port=PORT,
            use_reloader=False)
