import argparse
from pathlib import Path

from rsa.rsa import RSA
from rsa.sha import SHA
from rsa.prime import Prime


def init_options():
    arg_parser = argparse.ArgumentParser(description="""
        Sign a document with an electronic signature.
    """)
    arg_parser.add_argument('document', type=Path,
                            help='Path to the document')
    return arg_parser.parse_args()

if __name__ == '__main__':
    options = init_options()

    Prime_generator = Prime()
    p = Prime_generator.generate_prime(90)
    q = Prime_generator.generate_prime(90)
    e = Prime_generator.generate_prime(30)
    n = p * q
    rsa = RSA(n)
    d = rsa.get_private_key(e, p, q)

    with open(options.document) as f:
        message = f.read()
    message_hash = SHA().hash(message)

    signature = rsa.encrypt(message_hash, d)

    with open('public.key', 'w') as f:
        f.write(f'{n}\n{e}')
    
    with open(options.document.with_suffix('.sign'), 'w') as f:
        f.write(str(signature))