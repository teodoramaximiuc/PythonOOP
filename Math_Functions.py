import numpy as np
class MathFunctions:
    def pow (self, base, exponent):
        return base ** exponent
    def nth_fibbonaci (self, n):
        if n <= 0:
            return 0
        else :
            a = 0
            b = 1
            while(n > 1):
                c = a + b
                a = b
                b = c
                n -= 1
            return b
    def factorial (self, n):
        if n < 0:
            return None
        elif n == 0 or n == 1:
            return 1
        else:
            while n > 1:
                return n * self.factorial(n - 1)