from Common import Position


class Node:
    pass


#
# Expressions
#

class Expression(Node):
    def __init__(self, position: Position):
        self.position = position


class Literal(Expression):
    pass


class IntLiteral(Literal):
    def __init__(self, position: Position, value: int):
        super().__init__(position)
        self.value = value


class Location(Expression):
    pass


class LocationSimple(Location):
    def __init__(self, position: Position, name: str):
        super().__init__(position)
        self.value = name


class Call(Expression):
    def __init__(self, position: Position, func: Expression, args: [Expression]):
        super().__init__(position)
        self.func = func
        self.args = args


#
# Statements
#

class Statement(Node):
    def __init__(self, position: Position):
        self.position = position


class Assignment(Statement):
    def __init__(self, position: Position, target: Location, value: Expression):
        super().__init__(position)
        self.target = target
        self.value = value


class FunctionDefinition(Statement):
    def __init__(self, position: Position, name: str, args: [str], body: [Statement]):
        super().__init__(position)
        self.name = name
        self.args = args
        self.body = body


#
#
#

class Module(Node):
    def __init__(self, body: [Statement]):
        self.body = body
