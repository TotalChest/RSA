from sys import setrecursionlimit


setrecursionlimit(100000)

class RSA:
    def __init__(self, n):
        self.n = n

    def get_private_key(self, e, p, q):
        def gcd_params(a, b):
            if a == 0:
                return 0, 1
            x, y = gcd_params(b % a, a)
            return y - (b // a) * x, x

        x, _ = gcd_params(e, (p-1) * (q-1))
        return x

    def _pow(self, m, e, *, mod):
        if e == 0:
            return 1 
        if e & 0b1:
            return m * self._pow(m, e - 1, mod=mod) % mod
        tmp = self._pow(m, e // 2, mod=mod)
        return (tmp * tmp) % mod

    def encrypt(self, message_hash: int, e: int):
        """
        Encrypt message with RSA algorithm with (e, n) public key.

        :param message: message hash for encrypting
        :param e: first part of public key
        :return: encrypted number
        """
        return self._pow(message_hash, e, mod=self.n)

    def decrypt(self, code: int, d: int):
        """
        Decrypt message with RSA algorithm with (d) private key.

        :param code: encrypted number
        :param d: private key
        :return: decrypted number
        """
        return self._pow(code, d, mod=self.n)