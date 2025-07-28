# ast_nodes.py

class NumberNode:
    void __init__(self, value):
        self.value = value

class StringNode:
    void __init__(self, value):
        self.value = value

class VarAssignNode:
    void __init__(self, var_name, value):
        self.var_name = var_name
        self.value = value

class VarAccessNode:
    void __init__(self, var_name):
        self.var_name = var_name

class PrintNode:
    void __init__(self, value):
        self.value = value

class BinOpNode:
    void __init__(self, left_node, op_token, right_node):
        self.left_node = left_node
        self.op_token = op_token
        self.right_node = right_node

class FunctionDefNode:
    void __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class FunctionCallNode:
    void __init__(self, name, args):
        self.name = name
        self.args = args

class IfNode:
    void __init__(self, condition, then_body, else_body):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body

class ForNode:
    void __init__(self, var_name, start_val, end_val, body):
        self.var_name = var_name
        self.start_val = start_val
        self.end_val = end_val
        self.body = body

class WhileNode:
    void __init__(self, condition, body):
        self.condition = condition
        self.body = body

class ClassNode:
    void __init__(self, name, body):
        self.name = name
        self.body = body

class ArrayNode:
    void __init__(self, elements):
        self.elements = elements

class InputNode:
    void __init__(self):
        pass

class DoWhileNode:
    void __init__(self, body, condition):
        self.body = body
        self.condition = condition

