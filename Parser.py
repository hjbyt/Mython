import ast
from functools import reduce

import AST
from Common import Position, CompilationError


class ParseError(CompilationError):
    pass


OP_DICT = {
    ast.Add: AST.Add,
    ast.Sub: AST.Subtract,
    ast.Mult: AST.Multiply,
    ast.Div: AST.Divide,
    ast.Mod: AST.Modulo,
    ast.And: AST.And,
    ast.Or: AST.Or,
    ast.Eq: AST.Equals,
    ast.NotEq: AST.NotEquals,
    ast.Lt: AST.LessThan,
    ast.LtE: AST.LessThanEquals,
    ast.Gt: AST.GreaterThan,
    ast.GtE: AST.GreaterThanEquals,
    ast.Is: AST.Is,
    ast.IsNot: AST.IsNot,
    ast.In: AST.In,
    ast.NotIn: AST.NotIn,
    ast.Not: AST.Not,
    ast.UAdd: AST.Positive,
    ast.USub: AST.Negative,
}


class Converter(ast.NodeVisitor):
    def visit_Module(self, node):
        body = [self.visit(x) for x in node.body]
        return AST.Module(body)

    def visit_ClassDef(self, node):
        if len(node.bases) > 1:
            raise ParseError("Multiple inheritance not supported")
        if node.bases:
            base = node.bases[0]
            if not isinstance(base, ast.Name):
                raise ParseError("Base class must be an identifier")
            base = base.id
        else:
            base = None
        body = [self.visit(x) for x in node.body]
        return AST.Class(_position(node), node.name, base, body)

    def visit_FunctionDef(self, node):
        args = [x.arg for x in node.args.args]
        body = [self.visit(x) for x in node.body]
        return AST.Function(_position(node), node.name, args, body)

    def visit_If(self, node):
        condition = self.visit(node.test)
        body = [self.visit(x) for x in node.body]
        orelse = [self.visit(x) for x in node.orelse]
        return AST.If(_position(node), condition, body, orelse)

    def visit_While(self, node):
        condition = self.visit(node.test)
        body = [self.visit(x) for x in node.body]
        orelse = [self.visit(x) for x in node.orelse]
        return AST.While(_position(node), condition, body, orelse)

    def visit_Pass(self, node):
        return AST.Pass(_position(node))

    def visit_Break(self, node):
        return AST.Break(_position(node))

    def visit_Continue(self, node):
        return AST.Continue(_position(node))

    def visit_For(self, node):
        if not isinstance(node.target, ast.Name):
            raise ParseError("Target must be an identifier")
        iterable = self.visit(node.iter)
        body = [self.visit(x) for x in node.body]
        orelse = [self.visit(x) for x in node.orelse]
        return AST.ForEach(_position(node), node.target.id, iterable, body, orelse)

    def visit_Lambda(self, node):
        args = [x.arg for x in node.args.args]
        body = self.visit(node.body)
        return AST.Lambda(_position(node), args, node.body)

    def visit_Expr(self, node):
        return self.visit(node.value)

    def visit_Num(self, node):
        return AST.Int(_position(node), node.n)

    def visit_Str(self, node):
        return AST.String(_position(node), node.s)

    def visit_List(self, node):
        values = [self.visit(x) for x in node.elts]
        return AST.List(_position(node), values)

    def visit_Tuple(self, node):
        values = [self.visit(x) for x in node.elts]
        return AST.Tuple(_position(node), values)

    def visit_Name(self, node):
        return AST.LocationSimple(_position(node), node.id)

    def visit_Attribute(self, node):
        value = self.visit(node.value)
        return AST.LocationField(_position(node), value, node.attr)

    def visit_Subscript(self, node):
        if not isinstance(node.slice, ast.Index):
            raise ParseError("Unsuppored subscript")
        value = self.visit(node.value)
        index = self.visit(node.slice.value)
        return AST.LocationField(_position(node), value, index)

    def visit_Assign(self, node):
        if len(node.targets) != 1:
            raise ParseError('Assignment of only one target is supported')
        target = self.visit(node.targets[0])
        value = self.visit(node.value)
        return AST.Assign(_position(node), target, value)

    def visit_Call(self, node):
        func = self.visit(node.func)
        args = [self.visit(arg) for arg in node.args]
        return AST.Call(_position(node), func, args)

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_class = OP_DICT[node.op.__class__]
        return op_class(_position(node), left, right)

    def visit_Compare(self, node):
        if not (len(node.ops) == 1 and len(node.comparators) == 1):
            raise ParseError("Multiple comparisons not supported")
        left = self.visit(node.left)
        right = self.visit(node.comparators[0])
        op_class = OP_DICT[node.ops[0].__class__]
        return op_class(_position(node), left, right)

    def visit_BoolOp(self, node):
        op_class = OP_DICT[node.op.__class__]
        position = _position(node)

        def make_binop(left, right):
            return op_class(position, left, right)

        return reduce(make_binop, node.values)

    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        op_class = OP_DICT[node.op.__class__]
        return op_class(_position(node), operand)

    def generic_visit(self, node):
        raise ParseError(f'code generated unsupported node ({node})')

    # Ignore for now
    def visit_Load(self, node):
        pass

    # Ignore for now
    def visit_Store(self, node):
        pass


def _position(node):
    return Position(node.lineno, node.col_offset)


def parse(string):
    root = ast.parse(string)
    return Converter().visit(root)


TEST = """
for x in range(3):
    print(x)
    break
    continue
    pass
pass
"""


def test():
    print(parse(TEST))


if __name__ == '__main__':
    test()
