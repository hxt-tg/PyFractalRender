from Settings import *


class Complex:
    def __init__(self, real=0, imag=0):
        if isinstance(real, str):
            if real.endswith('i'):
                self.__real = 0
                self.__imag = float(real[:-1])
            else:
                self.__real = float(real)
                self.__imag = 0
        else:
            self.__real = real
            self.__imag = imag

    @property
    def real(self):
        return self.__real

    @real.setter
    def real(self, value):
        self.__real = value

    @property
    def imag(self):
        return self.__imag

    @imag.setter
    def imag(self, value):
        self.__imag = value

    @property
    def mod(self):
        return (self.real*self.real+self.imag*self.imag)**0.5

    @staticmethod
    def __remove_zero(num):
        num = str(num)
        if num[-2:] == '.0':
            num = num[:-2]
        return num

    def __str__(self):
        if self.real != 0:
            re = self.__remove_zero(self.real)
            im = '' if self.imag == 0 else ((
                '+i' if self.imag == 1 else '+' + Complex.__remove_zero(self.imag) + 'i') if self.imag > 0 else (
                '-i' if self.imag == -1 else Complex.__remove_zero(self.imag) + 'i'))
        else:
            re = '0' if self.imag == 0 else ''
            im = '' if self.imag == 0 else ((
                'i' if self.imag == 1 else Complex.__remove_zero(self.imag) + 'i') if self.imag > 0 else (
                '-i' if self.imag == -1 else Complex.__remove_zero(self.imag) + 'i'))
        return re + im

    def __add__(self, other):
        return Complex(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        return Complex(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other):
        return Complex(self.real * other.real - self.imag * other.imag, self.imag * other.real + self.real * other.imag)

    def __truediv__(self, other):
        res = Complex(0, 0)
        if other.real == 0 and other.imag == 0:
            raise ValueError(ERR_DIV_ZERO)
        res.real = (self.real * other.real + self.imag * other.imag) / (
                    other.real * other.real + other.imag * other.imag)
        res.imag = (self.imag * other.real - self.real * other.imag) / (
                    other.real * other.real + other.imag * other.imag)
        return res

    def __pow__(self, power, modulo=None):
        if power.imag != 0 or float(int(power.real)) != power.real:
            raise ValueError(ERR_NON_INT_POW)
        res = Complex(1, 0)
        for i in range(int(power.real)):
            res = res.__mul__(self)
        return res


if __name__ == '__main__':
    print(Complex(0, -1))
    print(Complex(0, 0))
    print(Complex(0, 1))
    print(Complex(-1, -1))
    print(Complex(-1, 0))
    print(Complex(-1, 1))
    print(Complex(0, 2))
    print(Complex(2, 0))
    print(Complex(2, 2))
