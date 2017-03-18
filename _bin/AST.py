from _bin.Lexer import Lexeme


class Node:
    def __init__(self, token: Lexeme):
        self.token = token


class Expression(Node):
    pass


class Literal(Expression):
    pass


class IntLiteral(Literal):
    def __init__(self, token: Lexeme):
        super().__init__(token)
        self.value = int(token.matched_string)

    def __str__(self):
        return str(self.value)

