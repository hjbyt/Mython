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


class Int(Literal):
    def __init__(self, position: Position, value: int):
        super().__init__(position)
        self.value = value


class String(Literal):
    def __init__(self, position: Position, value: str):
        super().__init__(position)
        self.value = value


class List(Literal):
    def __init__(self, position: Position, values: [Expression]):
        super().__init__(position)
        self.values = values


class Tuple(Literal):
    def __init__(self, position: Position, values: [Expression]):
        super().__init__(position)
        self.values = values


class Location(Expression):
    pass


class LocationSimple(Location):
    def __init__(self, position: Position, name: str):
        super().__init__(position)
        self.name = name


class LocationField(Location):
    def __init__(self, position: Position, value: Expression, field: str):
        super().__init__(position)
        self.value = value
        self.field = field


class LocationSubscript(Location):
    def __init__(self, position: Position, value: Expression, index: int):
        super().__init__(position)
        self.value = value
        self.index = index


class Call(Expression):
    def __init__(self, position: Position, func: Expression, args: [Expression]):
        super().__init__(position)
        self.func = func
        self.args = args


class BinOp(Expression):
    def __init__(self, position: Position, left: Expression, right: Expression):
        super().__init__(position)
        self.left = left
        self.right = right


class Add(BinOp):
    pass


class Subtract(BinOp):
    pass


class Multiply(BinOp):
    pass


class Divide(BinOp):
    pass


class Modulo(BinOp):
    pass


class And(BinOp):
    pass


class Or(BinOp):
    pass


class Comparison(BinOp):
    pass


class Equals(Comparison):
    pass


class NotEquals(Comparison):
    pass


class LessThan(Comparison):
    pass


class LessThanEquals(Comparison):
    pass


class GreaterThan(Comparison):
    pass


class GreaterThanEquals(Comparison):
    pass


class Is(BinOp):
    pass


class IsNot(BinOp):
    pass


class In(BinOp):
    pass


class NotIn(BinOp):
    pass


class UnaryOp(Expression):
    def __init__(self, position: Position, operand: Expression):
        super().__init__(position)
        self.operand = operand


class Not(UnaryOp):
    pass


class Positive(UnaryOp):
    pass


class Negative(UnaryOp):
    pass


class Lambda(Expression):
    def __init__(self, position: Position, args: [str], body: Expression):
        super().__init__(position)
        self.args = args
        self.body = body


#
# Statements
#

class Statement(Node):
    def __init__(self, position: Position):
        self.position = position


class Function(Statement):
    def __init__(self, position: Position, name: str, args: [str], body: [Statement]):
        super().__init__(position)
        self.name = name
        self.args = args
        self.body = body


class Class(Statement):
    def __init__(self, position: Position, name: str, base: str, body: [Statement]):
        super().__init__(position)
        self.name = name
        self.base = base
        self.body = body


class Assign(Statement):
    def __init__(self, position: Position, target: Location, value: Expression):
        super().__init__(position)
        self.target = target
        self.value = value


class If(Statement):
    def __init__(self, position: Position, condition: Expression, body: [Statement], orelse: [Statement]):
        super().__init__(position)
        self.condition = condition
        self.body = body
        self.orelse = orelse


class While(Statement):
    def __init__(self, position: Position, condition: Expression, body: [Statement], orelse: [Statement]):
        super().__init__(position)
        self.condition = condition
        self.body = body
        self.orelse = orelse


class ForEach(Statement):
    def __init__(self, position: Position, target: str, iterable: Expression, body: [Statement], orelse: [Statement]):
        super().__init__(position)
        self.target = target
        self.iterable = iterable
        self.body = body
        self.orelse = orelse


class Break(Statement):
    pass


class Continue(Statement):
    pass


class Pass(Statement):
    pass


#
#
#

class Module(Node):
    def __init__(self, body: [Statement]):
        self.body = body
