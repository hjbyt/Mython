from Lexer import lex, Lexeme
from Common import CompilationError
import parsimonious.utils
from parsimonious.grammar import TokenGrammar, NodeVisitor


class MythonSyntaxError(CompilationError):
    pass


_GRAMMAR = """
literal = int_literal / string_literal / boolean_literal / none_literal
int_literal = "INT"
string_literal = "STRING"
boolean_literal = "TRUE" / "FALSE"
none_literal = "NONE"
"""
GRAMMAR = TokenGrammar(_GRAMMAR)


class Token(parsimonious.utils.Token):
    def __init__(self, lexeme: Lexeme):
        super().__init__(lexeme.type.name)
        self.lexeme = lexeme


# class Analyzer(NodeVisitor):
#     def visit_literal(self, node, _):
#         pass
#
#     def visit_int_literal(self, node, _):
#         print(int(node.text[0].lexeme.matched_string))

def parse(string):
    lexemes = lex(string)
    tokens = [Token(x) for x in lexemes]
    parse_tree = GRAMMAR.parse(tokens)
    # Analyzer().visit(parsed)
    return parse_tree


TEST_STRING = """
5
"""


def test():
    print(parse(TEST_STRING))


if __name__ == '__main__':
    test()
