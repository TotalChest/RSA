# RSA (Rivest–Shamir–Adleman)
RSA public-key cryptosystem implementation

## Algorithms
- RSA (Rivest–Shamir–Adleman)
- SHA-1 (Secure Hash Algorithm 1)
- Miller-Rabin prime test

## Usage
#### Sign a document with the digital signature (RSA)
```bash
python encrypt.py <document>
```

The output will be a document signature and a public decryption key

#### Check the digital signature of a document (RSA)
```bash
python decrypt.py --key public.key <document> <signature>
```

If everything is ok, the output is 'Success! Document is genuine.' else output is 'Fail! Document is not genuine.'

