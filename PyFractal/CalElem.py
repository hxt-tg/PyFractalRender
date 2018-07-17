from PyFractal.Complex import Complex

'''
[Calculate Structure]
  +------+--------+----+--------+------+
  |      | lvalue |    | rvalue |      |
  | ltag |        | op |        | rtag |
  |      |  lcal  |    |  rcal  |      |
  +------+--------+----+--------+------+

[Tag]
  0 for NULL(only rtag), 1 for NUM, 2 for VAR and 3 for CalTree
'''


class CalElem:
    TK_NULL = 0
    TK_COM = 1
    TK_VAR = 2
    TK_TREE = 3

    OP_ADD = 4
    OP_SUB = 5
    OP_MUL = 6
    OP_DIV = 7
    OP_POW = 8

    TK_DESCRIBE = ['', 'NUM', 'z', 'TREE', '+', '-', '*', '/', '^', 'ERR']

    def __init__(self):
        self.__ltag = CalElem.TK_NULL
        self.__rtag = CalElem.TK_NULL
        self.__ltree = None
        self.__rtree = None
        self.__lvalue = None
        self.__rvalue = None
        self.__op = None

    def add_lchild(self):
        node = CalElem()
        self.__ltree = node
        self.__ltag = CalElem.TK_TREE
        return node

    def add_rchild(self):
        node = CalElem()
        self.__rtree = node
        self.__rtag = CalElem.TK_TREE
        return node

    def add_lparent(self):
        node = CalElem()
        node.__ltree = self
        node.__ltag = CalElem.TK_TREE
        return node

    def set_lvalue(self, val):
        if isinstance(val, Complex):
            self.__ltag = CalElem.TK_COM
            self.__lvalue = val
        else:
            if val == 'z':
                self.__ltag = CalElem.TK_VAR
            else:
                self.__ltag = CalElem.TK_COM
                self.__lvalue = Complex(val)

    def set_rvalue(self, val):
        if isinstance(val, Complex):
            self.__rtag = CalElem.TK_COM
            self.__rvalue = val
        else:
            if val == 'z':
                self.__rtag = CalElem.TK_VAR
            else:
                self.__rtag = CalElem.TK_COM
                self.__rvalue = Complex(val)

    def set_lchild(self, e):
        self.__ltag = CalElem.TK_TREE
        self.__ltree = e

    def set_rchild(self, e):
        self.__rtag = CalElem.TK_TREE
        self.__rtree = e

    def set_op(self, src):
        if src == '+':
            self.__op = CalElem.OP_ADD
        elif src == '-':
            self.__op = CalElem.OP_SUB
        elif src == '*':
            self.__op = CalElem.OP_MUL
        elif src == '/':
            self.__op = CalElem.OP_DIV
        elif src == '^':
            self.__op = CalElem.OP_POW

    def get_op(self):
        if self.__op == CalElem.OP_ADD:
            return '+'
        elif self.__op == CalElem.OP_SUB:
            return '-'
        elif self.__op == CalElem.OP_MUL:
            return '*'
        elif self.__op == CalElem.OP_DIV:
            return '/'
        elif self.__op == CalElem.OP_POW:
            return '^'
        return ' '

    def get_lvalue(self):
        return self.__lvalue

    def get_rvalue(self):
        return self.__rvalue

    def get_rtree(self):
        return self.__rtree

    def get_ltree(self):
        return self.__ltree

    def get_ltag(self):
        return self.__ltag

    def get_rtag(self):
        return self.__rtag

    @staticmethod
    def parse_float(src):
        try:
            return float(src)
        except ValueError:
            return None

    def value_of(self, z):
        lval = self.__lvalue if self.__ltag == CalElem.TK_COM else \
            (z if self.__ltag == CalElem.TK_VAR else self.__ltree.value_of(z))
        rval = self.__rvalue if self.__rtag == CalElem.TK_COM else \
            (z if self.__rtag == CalElem.TK_VAR else (
                None if self.__rtag == CalElem.TK_NULL else self.__rtree.value_of(z)))
        if rval is None:
            return lval
        if self.__op == CalElem.OP_ADD:
            return lval + rval
        elif self.__op == CalElem.OP_SUB:
            return lval - rval
        elif self.__op == CalElem.OP_MUL:
            return lval * rval
        elif self.__op == CalElem.OP_DIV:
            return lval / rval
        elif self.__op == CalElem.OP_POW:
            return lval ** rval
        else:
            return None

    def __str__(self):
        ls = str(self.__lvalue) if self.__ltag == CalElem.TK_COM else (
            str(self.__ltree) if self.__ltag == CalElem.TK_TREE else CalElem.TK_DESCRIBE[self.__ltag])
        rs = str(self.__rvalue) if self.__rtag == CalElem.TK_COM else (
            str(self.__rtree) if self.__rtag == CalElem.TK_TREE else CalElem.TK_DESCRIBE[self.__rtag])
        return '(' + ls + CalElem.TK_DESCRIBE[self.__op] + rs + ')'


if __name__ == '__main__':
    root = CalElem()
    b = root.add_lchild()
    a = b.add_rchild()
    root.set_rvalue('3')
    root.set_op('+')
    b.set_lvalue('z')
    b.set_op('*')
    a.set_lvalue('5')
    a.set_op('+')
    a.set_rvalue('z')
    print(root)
    print(root.value_of(Complex(1)))
    try:
        print(root.value_of(Complex(1)))
    except Exception as e:
        print(e.args[0], )


