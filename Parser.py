import ast
import AST
from Common import Position, CompilationError


class ParseError(CompilationError):
    pass


class Converter(ast.NodeVisitor):
    def visit_Module(self, node):
        body = [self.visit(x) for x in node.body]
        return AST.Module(body)

    def visit_FunctionDef(self, node):
        args = [x.arg for x in node.args.args]
        body = [self.visit(x) for x in node.body]
        return AST.FunctionDefinition(_position(node), node.name, args, body)

    def visit_Expr(self, node):
        return self.visit(node.value)

    def visit_Num(self, node):
        return AST.IntLiteral(_position(node), node.n)

    def visit_Name(self, node):
        return AST.LocationSimple(_position(node), node.id)

    def visit_Assign(self, node):
        if len(node.targets) != 1:
            raise ParseError('Assignment of only one target is supported')
        target = self.visit(node.targets[0])
        value = self.visit(node.value)
        return AST.Assignment(_position(node), target, value)

    def visit_Call(self, node):
        func = self.visit(node.func)
        args = [self.visit(arg) for arg in node.args]
        return AST.Call(_position(node), func, args)

    def generic_visit(self, node):
        print(f"generic: {node}")
        super().generic_visit(node)

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
def main(x):
    y = 5
    print(y)
"""


def test():
    print(parse(TEST))


if __name__ == '__main__':
    test()
