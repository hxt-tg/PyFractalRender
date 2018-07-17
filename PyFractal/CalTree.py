from PyFractal.CalElem import CalElem
from PyFractal.Complex import Complex
from Settings import *

NUM_MAX = 10
EXP_MAX = 200
OP_SET = ['+', '-', '*', '/', '(', ')', '^']
VALID_SET = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'i', 'z', '^', 'e',
             '.', '+', '-', '*', '/', '(', ')']


def _in_op(x):
    for i in OP_SET:
        if i == x:
            return True
    return False


class CHK_MODE:
    NUM_MODE = 0
    OP_MODE = 1


class ERR_MSG:
    RIGHT = 0               # No error */
    INVALID_CHAR = 1        # Invalid characters
    INVALID_DOT = 2         # Invalid dot like  ..	.<num>.
    LOST_CLOSE_BRACKET = 3  # No open bracket
    LOST_OPEN_BRACKET = 4   # No close bracket
    LOST_OPND = 5           # No operand  [+,-,*,/][),+,*,/] (+   (*   (/ */
    LOST_OPND_MINUS = 6     # No operator [+,-,*,/]-
    NUM_OVERFLOW = 7        # Number is too long
    UNEXPECTED_DOT = 8      # Unexpected dot  .<op>
    DIV_ZERO = 8            # Divided by zero  .<op>


def _check_exp(src):
    if len(src.strip()) == 0:
        raise ValueError(ERR_REQUIRE_EXP)
    # Check invalid char
    for i, s in enumerate(src):
        if s not in VALID_SET:
            raise ValueError(_error_process(ERR_MSG.INVALID_CHAR, i))

    # Lost operand at the end of string
    if src[-1] in ['+', '-', '*', '/', '^']:
        raise ValueError(_error_process(ERR_MSG.LOST_OPND, len(src)))

    src += ';'
    spos = 0
    chk_mode = CHK_MODE.OP_MODE
    chk_bracket = 0     # Bracket fitting
    first_num_pos = 0   # Number overflow
    chk_dot = 0         # Numbers of dot
    chk_i = 0
    first_i_pos = 0
    chk_e = 0
    first_e_pos = 0

    # Lost operand at the start of string
    if src[0] in ['+', '*', '/', '^']:
        raise ValueError(_error_process(ERR_MSG.LOST_OPND, -1))
    if src[0] == 'e':
        raise ValueError(_error_process(ERR_START_WITH_E, -1))

    while spos < len(src):
        if not _in_op(src[spos]):  # Operands
            # Records first num's pos
            if chk_mode == CHK_MODE.OP_MODE:
                first_num_pos = spos
            chk_mode = CHK_MODE.NUM_MODE
            if src[spos] == '.':
                if not '0' <= src[spos + 1] <= '9':
                    # .[<op>,i,e,z]
                    raise ValueError(_error_process(ERR_MSG.UNEXPECTED_DOT, spos))
                chk_dot += 1
            elif src[spos] == 'i':
                chk_i += 1
                if chk_i == 1:
                    first_i_pos = spos
            elif src[spos] == 'z':
                if ('0' <= src[spos + 1] <= '9') or src[spos + 1] == 'z' or src[spos + 1] == 'i':
                    raise ValueError(_error_process(ERR_MSG.LOST_OPND, spos + 1))
                elif src[spos] == 'e':
                    chk_e += 1
                    if chk_e == 1:
                        first_e_pos = spos
                    # <num>e[<op>,i,e,z,.]
                    if (not '0' <= src[spos + 1] <= '9') and src[spos + 1] != '-':
                        raise ValueError(_error_process('', spos))
                    # <num>e-[<op>,i,e,z,.]
                    if (not '0' <= src[spos + 2] <= '9') and src[spos + 1] == '-':
                        raise ValueError(_error_process('', spos))
                else:
                    pass
        else:
            chk_mode = CHK_MODE.OP_MODE
            first_num_pos = spos
            chk_dot = 0
            chk_i = 0
            chk_e = 0
            if src[spos] == ')':
                chk_bracket -= 1
            elif src[spos] == '(':
                # (+   (*   (/
                if spos < len(src) - 1:
                    if _in_op(src[spos + 1]) and (src[spos + 1] == '+' or src[spos + 1] == '*' or src[spos + 1] == '/'):
                        raise ValueError(_error_process(ERR_MSG.LOST_OPND, spos + 1))
                chk_bracket += 1
            else:
                if spos < len(src) - 1:
                    if len(src) == spos or _in_op(src[spos + 1]) and src[spos + 1] != '(':
                        # [+,-,*,/][),+,-,*,/]
                        if src[spos + 1] == '-':
                            raise ValueError(_error_process(ERR_MSG.LOST_OPND_MINUS, spos + 1))
                        raise ValueError(_error_process(ERR_MSG.LOST_OPND, spos + 1))
            if src[spos + 1] == 'e':
                spos += 1
                raise ValueError(_error_process(ERR_UNEXPECTED_E, spos))
        # ())
        if chk_bracket < 0:
            raise ValueError(_error_process(ERR_MSG.LOST_OPEN_BRACKET, spos))
        # ..	.<num>.
        if chk_dot > 1:
            raise ValueError(_error_process(ERR_MSG.INVALID_DOT, spos))
        # <num>i<num>i
        if chk_i > 1:
            raise ValueError(_error_process(ERR_I, first_i_pos + 1))
        # <num>e<num>e<num>
        if chk_e > 1:
            raise ValueError(_error_process(ERR_E, first_e_pos + 1))
        # Number overflow
        if spos - first_num_pos >= NUM_MAX:
            raise ValueError(_error_process(ERR_MSG.NUM_OVERFLOW, spos))
        if spos > len(src):
            break
        spos += 1
    if chk_bracket > 0 and chk_dot <= 1:
        # (()
        raise ValueError(_error_process(ERR_MSG.LOST_CLOSE_BRACKET, spos))


def _pre_process(src):
    tp_str = ''
    i = 0
    if src[i] == '-':
        tp_str += '0'
    while i < len(src) - 1:
        tp_str += src[i]
        if _in_op(src[i]):
            # ")(" -> ")*("
            # ")<num>" -> ")*<num>"
            if src[i] == ')' and ('0' <= src[i+1] <= '9' or src[i+1] in ['(', 'i', 'z']):
                tp_str += '*'
                if src[i+1] == 'i':
                    tp_str += '1'
            # "(-" -> "(0-)"
            if src[i] == '(' and src[i + 1] in ['-', ')']:
                tp_str += '0'
            # "[+,-,*,/]i"
            if src[i] in ['+', '-', '*', '/', '^'] and src[i+1] == 'i':
                tp_str += '1'
        else:
            # "<num>(" -> "<num>*("
            if src[i + 1] in ['(', 'i', 'z']:
                tp_str += '*'
                if src[i + 1] == 'i':
                    tp_str += '1'
        i += 1
    tp_str += src[i]
    return tp_str


def _get_order(op1, op2):
    if op1 == op2:
        return 1 if op1 == '^' else -1
    if op1 == '+' or op1 == '-':
        order1 = 3
    elif op1 == '*' or op1 == '/':
        order1 = 2
    else:
        order1 = 1
    if op2 == '+' or op2 == '-':
        order2 = 3
    elif op2 == '*' or op2 == '/':
        order2 = 2
    else:
        order2 = 1
    return -1 if order1 == order2 else order1 - order2


def _error_process(err, pos):
    if isinstance(err, str):
        return ((ERR_AT_CHAR + '[' + str(pos) + ']:') if pos >= 0 else ERR_BEFORE_EXP + ': ') + str(err)
    else:
        if err == ERR_MSG.RIGHT:
            return ""
        else:
            if err != ERR_MSG.DIV_ZERO:
                err_str = ((ERR_AT_CHAR + '[' + str(pos) + ']: ') if pos >= 0 else ERR_BEFORE_EXP + ': ')
            else:
                err_str = ''
            if err == ERR_MSG.INVALID_CHAR:
                err_str += ERR_INVALID_CHAR
            elif err == ERR_MSG.INVALID_DOT:
                err_str += ERR_INVALID_DOT
            elif err == ERR_MSG.LOST_CLOSE_BRACKET:
                err_str += ERR_LOST_CLOSE_BRACKET
            elif err == ERR_MSG.LOST_OPEN_BRACKET:
                err_str += ERR_LOST_OPEN_BRACKET
            elif err == ERR_MSG.LOST_OPND:
                err_str += ERR_LOST_OPND
            elif err == ERR_MSG.LOST_OPND_MINUS:
                err_str += ERR_LOST_OPND_MINUS
            elif err == ERR_MSG.NUM_OVERFLOW:
                err_str += ERR_NUM_OVERFLOW
            elif err == ERR_MSG.UNEXPECTED_DOT:
                err_str += ERR_UNEXPECTED_DOT
            elif err == ERR_MSG.DIV_ZERO:
                err_str += ERR_DIV_ZERO
            else:
                pass
        return err_str


class CalTree:
    def __init__(self, exp_str):
        self.__root = CalElem()
        _check_exp(exp_str[:])
        self.parseCalTree(_pre_process(exp_str))

    def parseCalTree(self, src):
        s = src.lower()
        cur = CalElem()
        s_cal = [cur]
        i = 0
        while i < len(s):
            if s[i] == '(':
                cur = cur.add_lchild() if cur.get_ltag() == CalElem.TK_NULL else cur.add_rchild()
                s_cal.append(cur)
            elif s[i] == ')':
                s_cal.pop()
                cur = s_cal[-1]
            elif s[i] in ['+', '-', '*', '/', '^']:
                if cur.get_rtag() != CalElem.TK_NULL:
                    if _get_order(cur.get_op(), s[i]) < 0:
                        cur = s_cal.pop()
                        cur = cur.add_lparent()
                        if len(s_cal) > 0:
                            temp = s_cal[-1]
                            if temp.get_ltag() == CalElem.TK_TREE and temp.get_ltree() == cur.get_ltree():
                                temp.set_lchild(cur)
                            else:
                                temp.set_rchild(cur)
                    else:
                        if cur.get_rtag() == CalElem.TK_COM:
                            val = cur.get_rvalue()
                            cur = cur.add_rchild()
                            cur.set_lvalue(val)
                        else:
                            cur = cur.add_rchild()
                            cur.set_lvalue('z')
                    s_cal.append(cur)
                cur.set_op(s[i])
            elif s[i] == 'z':
                if cur.get_ltag() == CalElem.TK_NULL:
                    cur.set_lvalue('z')
                else:
                    cur.set_rvalue('z')
            else:   # Numbers
                s_num = ''
                s_num += s[i]
                i += 1
                while True:
                    if s[i-1] == 'e' and s[i] == '-' and '0' <= s[i+1] <= '9':
                        s_num += s[i]
                        i += 1
                        continue
                    if i < len(s) and ('0' <= s[i] <= '9' or s[i] in ['e', '.', 'i']):
                        s_num += s[i]
                        i += 1
                    else:
                        break
                i -= 1
                if cur.get_ltag() == CalElem.TK_NULL:
                    cur.set_lvalue(s_num)
                else:
                    cur.set_rvalue(s_num)
            i += 1
        while len(s_cal) > 0:
            self.__root = s_cal.pop()

    def value_of(self, z):
        return self.__root.value_of(z)

    def __str__(self):
        return str(self.__root)


if __name__ == '__main__':
    exp = CalTree("z^2+0.3")
    print(exp.value_of(Complex(0.3, 0.5)))
    for i in range(400):
        for j in range(400):
            exp.value_of(Complex(0.3, 0.5))
        print(i)
