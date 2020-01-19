"""A Flask-based Anno notebook server.
"""

from   anno.anno.app import app
import argparse
import webbrowser


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--nopen',
                        help='Open browser tab.',
                        action='store_true')
    parser.add_argument('--port',
                        type=int,
                        help='HTTP address port.',
                        default=5000)
    args = parser.parse_args()

    if not args.nopen:
        webbrowser.open_new_tab(f'http://localhost:{args.port}/')

    app.run(debug=True,
            host='0.0.0.0',
            port=args.port,
            use_reloader=False)
