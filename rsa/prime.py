from random import randint


class Prime:
    small_primes = (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53,
                    59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109,
                    113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
                    179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233,
                    239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293,
                    307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367,
                    373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433,
                    439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499,
                    503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577,
                    587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643,
                    647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719,
                    727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797,
                    809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863,
                    877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947,
                    953, 967, 971, 977, 983, 991, 997)                

    def _pow(self, m, e, *, mod):
        if e == 0:
            return 1 
        if e & 0b1:
            return m * pow(m, e - 1, mod=mod) % mod
        tmp = pow(m, e // 2, mod=mod)
        return (tmp * tmp) % mod

    def _pow_test(self, a, b, *, mod):
        s = 0
        t = b
        while not t & 0x1:
            s += 1
            t >>= 1
        
        tmp = self._pow(a, t, mod=mod)
        if tmp == 1:
            return True
        for _ in range(s):
            if tmp == b:
                return True
            tmp = tmp * tmp % mod
        return False

    def RabinMillerWitness(self, witness, possible):
        """
        Return True if possible may be prime.
        Return False if if is composite.
        """
        return self._pow_test(witness, possible - 1, mod=possible)

    def generate_prime(self, size):
        """Generate an integer of size bits that is probably prime."""
        steps = max(10 * size, 64)
        find_prime = False
        while not find_prime:
            possible_prime = randint(2 ** (size-1), 2 ** size - 1) | 0x1
            find_prime = True
            for small_prime in self.small_primes:
                if not possible_prime % small_prime:
                    find_prime = False
                    break
            else:
                for _ in range(steps):
                    witness = randint(2, possible_prime) | 0x1
                    if not self.RabinMillerWitness(witness, possible_prime):
                        find_prime = False
                        break

        return possible_prime
