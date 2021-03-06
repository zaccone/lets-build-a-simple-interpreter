# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
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
        # token type: INTEGER, PLUS, or EOF
        self.type = type
        # token value: 0, 1, 2. 3, 4, 5, 6, 7, 8, 9, '+', or None
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS '+')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Interpreter(object):
    def __init__(self, text):
        # client string input, e.g. "3+5"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        # current token instance
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """

        def build_number():
            number = 0
            pos = self.pos
            for candidate in text[pos:]:
                if candidate.isdigit():
                    number *= 10
                    number += int(candidate)
                    self.pos += 1
                else:
                    break
            return number

        def skip_spaces():
            while self.pos < len(text):
                current_char = text[self.pos]
                if current_char.isspace():
                    self.pos += 1
                else:
                    return

        text = self.text

        skip_spaces()

        # is self.pos index past the end of the self.text ?
        # if so, then return EOF token because there is no more
        # input left to convert into tokens
        if self.pos > len(text) - 1:
            return Token(EOF, None)

        # get a character at the position self.pos and decide
        # what token to create based on the single character
        # if the character is a digit then convert it to
        # integer, create an INTEGER token, increment self.pos
        # index to point to the next character after the digit,
        # and return the INTEGER token

        current_char = text[self.pos]

        if current_char.isdigit():

            number = build_number()
            token = Token(INTEGER, number)
            return token

        if current_char in CHAR_OPERATORS:
            operator = CHAR_OPERATORS[current_char]
            token = Token(operator, current_char)
            self.pos += 1
            return token

        self.error()

    def term(self):
        token = self.current_token
        self.eat([INTEGER])
        return token.value

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type in token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        """expr -> INTEGER PLUS INTEGER"""
        self.current_token = self.get_next_token()

        result = self.term()
        while self.current_token.type is not EOF:
            op = self.current_token
            self.eat(OPERATORS.keys())

            right = self.term()

            if op.type in OPERATORS:
                result = OPERATORS[op.type](result, right)
            else:
                self.error()

        return result


def main():
    while True:
        try:
            # To run under Python3 replace 'raw_input' call
            # with 'input'
            text = raw_input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()
