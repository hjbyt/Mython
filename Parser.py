from Lexer import lex, LexemeType
from Common import CompilationError
import AST


class SyntaxError(CompilationError):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = list(tokens)

    def next_is_eof(self):
        return len(self.tokens) == 0

    def next_is(self, type: LexemeType):
        try:
            return self.tokens[-1].type == type
        except IndexError:
            raise SyntaxError('EOF not expected')

    def pop(self):
        try:
            return self.tokens.pop()
        except IndexError:
            raise SyntaxError('EOF not expected')

    def match(self, expected_type: LexemeType):
        token = self.pop()
        if token.type != expected_type:
            raise SyntaxError('Unexpected token (%s)' % token)
        return token

    def parse_expression(self):
        pass

    def parse_int(self):
        token = self.match(LexemeType.INT)
        return AST.IntLiteral(token)


TEST_STRING = """
5
"""


def test():
    parser = Parser(lex(TEST_STRING))
    print(parser.parse_int())


if __name__ == '__main__':
    test()
