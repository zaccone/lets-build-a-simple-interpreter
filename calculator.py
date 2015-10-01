#!/usr/bin/python3

INTEGER, PLUS, MINUS, MUL, DIV, EOF = ('INTEGER', 'PLUS', 'MINUS', 'MUL',
                                       'DIV', 'EOF')

OPERATORS = {
    PLUS: lambda x, y: x + y,
    MINUS: lambda x, y: x - y,
    MUL: lambda x, y: x * y,
    DIV: lambda x, y: x/y
}

CHAR_OPERATORS = {
    '+': PLUS,
    '-': MINUS,
    '*': MUL,
    '/': DIV
}


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value


class Interpreter(object):
    def __init__(self, text):
        self.text = text
        self.length = len(text)
        self.pos = 0

    def current_character(self):
        try:
            return self.text[self.pos]
        except IndexError:
            return None

    def advance(self):
        self.pos += 1

    def integer(self):
        c = self.current_character()
        if not c:
            return None

        result = 0
        while c and c.isdigit():
            result *= 10
            result += int(c)
            self.advance()
            c = self.current_character()
        else:
            return result

    def operator(self):
        c = self.current_character()
        self.advance()
        if c and c in CHAR_OPERATORS:
            return CHAR_OPERATORS[c], c
        else:
            msg = "Character {c} is not an operator".format(c=c)
            raise Exception(msg)

    # TODO(zaccone): Use expected argument for sanity checks
    def get_token(self, expected):
        if self.current_character() is None:
            return Token(EOF, None)

        while self.current_character():
            if self.current_character().isspace():
                self.advance()
            elif self.current_character().isdigit():
                return Token(INTEGER, self.integer())
            else:
                operator, operator_char = self.operator()
                return Token(operator, operator_char)

        else:
            return Token(EOF, None)

    def eval(self):

        left = self.get_token([INTEGER])

        operator = self.get_token(OPERATORS.keys())

        right = self.get_token([INTEGER])

        operator = OPERATORS[operator.type]
        return operator(left.value, right.value)


def main():
    while True:
        try:
            # To run under Python3 replace 'raw_input' call
            # with 'input'
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.eval()
        print(result)


if __name__ == '__main__':
    main()
