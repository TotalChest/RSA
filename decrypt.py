import argparse
from pathlib import Path

from rsa.rsa import RSA
from rsa.sha import SHA


def init_options():
    arg_parser = argparse.ArgumentParser(description="""
        Check electronic signature of a document.
    """)
    arg_parser.add_argument('document', type=Path,
                            help='Path to the document')
    arg_parser.add_argument('signature', type=Path,
                            help='Path to the signature')
    arg_parser.add_argument('--key', required=True, type=Path,
                            help='Path to the public key')
    return arg_parser.parse_args()

if __name__ == '__main__':
    options = init_options()

    with open(options.key) as f:
        n, e = f.read().split('\n')
        n = int(n)
        e = int(e)
    rsa = RSA(n)

    with open(options.document) as f:
        message = f.read()
    message_hash = SHA().hash(message)

    with open(options.signature) as f:
        if message_hash == rsa.decrypt(int(f.read()), e):
            print('Authentication succeeded')
        else:
            print('Authentication failed')

    