"""============================================================================
A Flask-based Anno notebook server.
============================================================================"""

from   anno.anno.app import app
from   anno.anno.config import generate_config
import argparse
import os
import shutil
import socket
import webbrowser


# -----------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bundle',
                        help='Use UNIX\'s `zip` to compress current '
                             'directory.',
                        action='store_true',
                        required=False)
    parser.add_argument('--generate-config',
                        help='Generate configuration file.',
                        action='store_true',
                        required=False)
    parser.add_argument('--nopen',
                        help='Open browser tab.',
                        action='store_true',
                        required=False)
    parser.add_argument('--port',
                        type=int,
                        help='HTTP address port.',
                        default=5000,
                        required=False)
    parser.add_argument('--pw',
                        help='Require password with `--bundle` command.',
                        action='store_true',
                        required=False)
    args = parser.parse_args()

    if args.bundle:
        if not shutil.which('zip'):
            msg = 'Anno requires UNIX\'s `zip` command to bundle: ' \
                  'https://linux.die.net/man/1/zip.'
            raise ValueError(msg)
        if args.generate_config:
            msg = 'Conflicting arguments `--bundle` and `--generate-config`.'
            raise ValueError(msg)
        path = os.getcwd()
        _, directory = os.path.split(path)
        encrypt = '--encrypt' if args.pw else ''
        filename = f'{directory}_archive.zip'
        if os.path.exists(filename):
            msg = f'Bundling failed because "{filename}" already exists.'
            raise ValueError(msg)
        cmd = f'zip {encrypt} -r {filename} .'
        os.system(cmd)
        print(f'Notes in "{path}" compressed into "{filename}".')

    elif args.generate_config:
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
