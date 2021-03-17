from sys import setrecursionlimit


setrecursionlimit(100000)

class RSA:
    def __init__(self, n):
        self.n = n

    def get_private_key(self, e, p, q):
        def gcd_params(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x, y = gcd_params(b % a, a)
            return gcd, y - (b // a) * x, x

        _, x, _ = gcd_params(e, (p-1) * (q-1))
        return max(x, (p-1) * (q-1) + x)

    def _pow(self, a, n, *, mod):
        if n == 0:
            return 1 
        if n & 0b1:
            return self._pow(a, n - 1, mod=mod) * a % mod
        tmp = self._pow(a, n // 2, mod=mod)
        return (tmp * tmp) % mod

    def encrypt(self, message_hash: int, e: int):
        """
        Encrypt numbeer with RSA algorithm with (e, n) public key.

        :param message: number for encrypting
        :param e: first part of public key
        :return: encrypted number
        """
        return self._pow(message_hash, e, mod=self.n)

    def decrypt(self, code: int, d: int):
        """
        Decrypt number with RSA algorithm with (d) private key.

        :param code: number for decrypting
        :param d: private key
        :return: decrypted number
        """
        return self._pow(code, d, mod=self.n)