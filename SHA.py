
class SHA:
    BASE = 0xffffffff
    F = {
        0: lambda b, c, d: (b & c) | (~b & d),
        1: lambda b, c, d: b ^ c ^ d,
        2: lambda b, c, d: (b & c) | (b & d) | (c & d),
        3: lambda b, c, d: b ^ c ^ d
    }
    K = {
        0: 0x5A827999,
        1: 0x6ED9EBA1,
        2: 0x8F1BBCDC,
        3: 0xCA62C1D6
    }

    def _left_cyclic_rotate(self, number, count):
        def left_cyclic_shift(number):
            first_bit = 0x1 if (number & 0x80000000) else 0x0
            return ((number << 1) & self.BASE) | first_bit
        
        for _ in range(count):
            number = left_cyclic_shift(number)
        return number

    def _get_block(self, message):
        message_length = len(message)
        message = bytes(message.encode('utf-8'))

        for i in range(message_length // 64):
            yield message[i*64 : (i+1)*64]

        big_endian_length = bytes([
            (message_length & (0xff << shift)) >> shift
            for shift in range(56, -1, -8)
        ])
        remainder = message_length % 64
        if remainder > 55:
            yield message[-remainder:] + bytes([0x80] + [0] * (63-remainder))
            yield bytes([0] * 56) + big_endian_length
        else:
            yield (message[-remainder:]
                   + bytes([0x80] + [0] * (55-remainder))
                   + big_endian_length)

    def hash(self, message):
        """
        Calculate hash function SHA-1.

        :param message: text for hashing
        :returns: SHA-1 hash (160-bit)
        """
        h0 = 0x67452301
        h1 = 0xEFCDAB89
        h2 = 0x98BADCFE
        h3 = 0x10325476
        h4 = 0xC3D2E1F0

        for block in self._get_block(message):
            w = []
            for i in range(16):
                w.append(int.from_bytes(block[i*4 : (i+1)*4], 'big'))
            for i in range(16, 80):
                w.append(self._left_cyclic_rotate(
                    w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16],
                    1
                ))
            
            a = h0
            b = h1
            c = h2
            d = h3
            e = h4

            for i in range(80):
                f = self.F[i // 20]
                k = self.K[i // 20]

                temp = (self._left_cyclic_rotate(a, 5)
                    + f(b, c, d) + e + k + w[i]) & self.BASE
                e = d
                d = c
                c = self._left_cyclic_rotate(b, 30)
                b = a
                a = temp

            h0 = (h0 + a) & self.BASE
            h1 = (h1 + b) & self.BASE
            h2 = (h2 + c) & self.BASE
            h3 = (h3 + d) & self.BASE
            h4 = (h4 + e) & self.BASE

        binary_hash = f'{h0:032b}{h1:032b}{h2:032b}{h3:032b}{h4:032b}'
        return int(binary_hash, 2)