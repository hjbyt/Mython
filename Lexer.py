import re
from enum import Enum
from typing import NamedTuple

INDENTATION_SIZE = 4


class CompilationError(ValueError):
    pass


class LexError(CompilationError):
    pass


class LexemeType(Enum):
    DEF = re.compile("def")
    COLON = re.compile(":")
    LPAREN = re.compile(r"\(")
    RPAREN = re.compile(r"\)")

    INT = re.compile("([0-9]+)")
    ID = re.compile("[a-zA-Z][a-zA-Z0-9_]*")
    WHITESPACE = re.compile(" +")

    INDENT = '<INDENT>'
    DEDENT = '<DEDENT>'

    def __init__(self, regex):
        self.regex = regex

    def __repr__(self):
        return self.name


class Lexeme(NamedTuple):
    type: LexemeType
    line: int
    column: int
    matched_string: str


def lex(string):
    lines = string.splitlines()
    current_indentation_level = 0
    current_line = 0

    for line in lines:
        current_line += 1
        current_pos = 0

        # Check indentation
        lstripted_line = line.lstrip(' ')
        if lstripted_line == '':
            continue
        leading_space_count = len(line) - len(lstripted_line)
        line_indentation_level, remainder = divmod(leading_space_count, INDENTATION_SIZE)
        if remainder != 0:
            raise LexError("Invalid indentation at line %d" % current_line)

        indentation_diff = line_indentation_level - current_indentation_level
        indenetation_type = LexemeType.INDENT if indentation_diff >= 0 else LexemeType.DEDENT
        for _ in range(abs(indentation_diff)):
            yield Lexeme(indenetation_type, current_line, 0, '')
        current_indentation_level = line_indentation_level

        while current_pos < len(line):
            for lexeme_type in LexemeType:
                match = lexeme_type.regex.match(line, current_pos)
                if match:
                    matched_string = match.group()
                    if lexeme_type != LexemeType.WHITESPACE:
                        yield Lexeme(lexeme_type, current_line, current_pos, matched_string)

                    current_pos = match.end()

                    break
            else:
                raise LexError("Illegal character at line: %d, column: %d" % (current_line, current_pos))


test_string = """

def asdf():
    5

    4
7

"""


def test():
    for token in lex(test_string):
        print(token)


if __name__ == '__main__':
    test()
