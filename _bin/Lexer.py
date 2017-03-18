import re
from enum import Enum
from typing import NamedTuple
from Common import CompilationError

INDENTATION_SIZE = 4


class LexError(CompilationError):
    pass


class LexemeType(Enum):
    # Keywords
    CLASS = re.compile(r'class')
    DEF = re.compile('def')
    COLON = re.compile(':')
    LPAREN = re.compile(r'\(')
    RPAREN = re.compile(r'\)')
    LBRACKET = re.compile(r'\[')
    RBRACKET = re.compile(r'\]')
    LCURLY = re.compile(r'}')
    RCURLY = re.compile(r'}')
    ASSIGN = re.compile(r'=')
    EQ = re.compile(r'==')
    NEQ = re.compile(r'!=')
    GT = re.compile(r'>')
    GTE = re.compile(r'>=')
    LT = re.compile(r'<')
    LTE = re.compile(r'<=')
    PLUS = re.compile(r'\+')
    MINUS = re.compile(r'-')
    MULT = re.compile(r'\*')
    DIV = re.compile(r'/')
    MOD = re.compile(r'%')
    AND = re.compile(r'and')
    OR = re.compile(r'or')
    NOT = re.compile(r'not')
    IN = re.compile(r'in')
    IS = re.compile(r'is')
    DOT = re.compile(r'\.')
    COMMA = re.compile(r',')
    FOR = re.compile(r'for')
    WHILE = re.compile(r'while')
    CONTINUE = re.compile(r'continue')
    BREAK = re.compile(r'BREAK')
    IF = re.compile(r'if')
    ELSE = re.compile(r'else')
    ELIF = re.compile(r'elif')
    PASS = re.compile(r'pass')
    TRUE = re.compile(r'True')
    FALSE = re.compile(r'False')
    NONE = re.compile(r'None')
    RETURN = re.compile(r'return')
    LAMBDA = re.compile(r'lambda')
    # TODO: this might be used for short lambda syntax: 2*it instead of lambda x: 2*x.
    # IT = re.compile(r'it')

    # Literals
    STRING = re.compile(r'"([ -!#-\[\]-~]|(\\[tn\\\"]))*"')
    INT = re.compile('[0-9]+')
    # Symbols
    ID = re.compile('[a-zA-Z][a-zA-Z0-9_]*')

    # Ignored
    WHITESPACE = re.compile(' +')
    COMMENT = re.compile('#.*')

    # Error fallback
    INVALID = re.compile('.*')

    # Special block delimiters
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


def lex(string : str):
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
            raise LexError('Invalid indentation at line %d' % current_line)

        indentation_diff = line_indentation_level - current_indentation_level
        indenetation_type = LexemeType.INDENT if indentation_diff >= 0 else LexemeType.DEDENT
        for _ in range(abs(indentation_diff)):
            yield Lexeme(indenetation_type, current_line, 0, '')
        current_indentation_level = line_indentation_level

        while current_pos < len(line):
            for lexeme_type in LexemeType:
                if lexeme_type == LexemeType.INVALID:
                    raise LexError('Invalid character at line: %d, column: %d' % (current_line, current_pos))
                match = lexeme_type.regex.match(line, current_pos)
                if match:
                    matched_string = match.group()
                    if lexeme_type not in {LexemeType.WHITESPACE, LexemeType.COMMENT}:
                        yield Lexeme(lexeme_type, current_line, current_pos, matched_string)

                    current_pos = match.end()
                    break
