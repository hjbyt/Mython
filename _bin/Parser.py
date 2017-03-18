import parsimonious.utils
from parsimonious.grammar import TokenGrammar

from Common import CompilationError
from _bin.Lexer import lex, Lexeme


class MythonSyntaxError(CompilationError):
    pass


_GRAMMAR = """
test = or_test / lambdef
lambdef = "LAMBDA" arglist? "COLON" test
or_test = and_test ("OR" and_test)*
and_test = not_test ("AND" not_test)*
not_test = ("NOT" not_test) / comparison
comparison = expr (comp_op expr)*
comp_op = "LT" / "GT" / "EQ" / "GTE" / "LTE" / "NEQ" / "IN" / ("NOT" "IN") / "IS" / ("IS" "NOT")
expr = arith_expr
arith_expr = term (("PLUS" / "MINUS") term)*
term = factor (("MULT" / "DIV" / "MOD") factor)*
factor = (("PLUS" / "MINUS") factor) / atom_expr
atom_expr = atom trailer*
atom = ("LPAREN" test "RPAREN") / "ID" / literal
trailer = ("LPAREN" arglist? "RPAREN") / ("LBRACKET" test "RBRACKET") / ("DOT" "ID")
arglist = test ("COMMA" test)*

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
