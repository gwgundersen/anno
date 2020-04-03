"""============================================================================
A Flask-based Anno notebook server.
============================================================================"""

from   anno.anno.app import app
from   anno.anno.config import generate_config
import argparse
import socket
import webbrowser


# -----------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--nopen',
                        help='Open browser tab.',
                        action='store_true')
    parser.add_argument('--port',
                        type=int,
                        help='HTTP address port.',
                        default=5000)
    parser.add_argument('--generate-config',
                        help='Generate configuration file.',
                        action='store_true')
    args = parser.parse_args()

    if args.generate_config:
        fpath = generate_config()
        msg   = f'Writing default config to: {fpath}'
        print(msg)
    else:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            result = sock.connect_ex(('127.0.0.1', args.port))
            if result == 0:
                raise OSError(f'Port {args.port} already in use.')
        if not args.nopen:
            webbrowser.open_new_tab(f'http://localhost:{args.port}/')

        app.run(debug=True,
                host='0.0.0.0',
                port=args.port,
                use_reloader=False)
