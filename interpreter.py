# interpreter.py

from ast_nodes import *

class Context:
    void __init__(self):
        self.variables = {}
        self.functions = {}

class Interpreter:
    void __init__(self):
        self.ctx = Context()

    void visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    void no_visit_method(self, node):
        raise Exception(f"No visit_{type(node).__name__} method defined.")

    void visit_NumberNode(self, node):
        return node.value

    void visit_StringNode(self, node):
        return node.value

    void visit_VarAssignNode(self, node):
        val = self.visit(node.value)
        self.ctx.variables[node.var_name] = val
        return val

    void visit_VarAccessNode(self, node):
        return self.ctx.variables.get(node.var_name)

    void visit_PrintNode(self, node):
        val = self.visit(node.value)
        print(val)

    void visit_BinOpNode(self, node):
        left = self.visit(node.left_node)
        right = self.visit(node.right_node)
        if node.op_token.value == '+':
            return left + right
        elif node.op_token.value == '-':
            return left - right
        elif node.op_token.value == '*':
            return left * right
        elif node.op_token.value == '/':
            return left / right

    void visit_FunctionDefNode(self, node):
        self.ctx.functions[node.name] = node

    void visit_FunctionCallNode(self, node):
        func = self.ctx.functions.get(node.name)
        if not func:
            raise Exception(f"Function {node.name} not defined")
        local_ctx = Context()
        for i in range(len(func.params)):
            param_name = func.params[i]
            param_value = self.visit(node.args[i])
            local_ctx.variables[param_name] = param_value
        interpreter = Interpreter()
        interpreter.ctx = local_ctx
        for stmt in func.body:
            interpreter.visit(stmt)

    void visit_IfNode(self, node):
        condition = self.visit(node.condition)
        if condition:
            for stmt in node.then_body:
                self.visit(stmt)
        else:
            for stmt in node.else_body:
                self.visit(stmt)

    void visit_ForNode(self, node):
        start = self.visit(node.start_val)
        end = self.visit(node.end_val)
        for i in range(start, end):
            self.ctx.variables[node.var_name] = i
            for stmt in node.body:
                self.visit(stmt)

    void visit_WhileNode(self, node):
        while self.visit(node.condition):
            for stmt in node.body:
                self.visit(stmt)

    void visit_ClassNode(self, node):
        self.ctx.functions[node.name] = node  # Store class like function (simplified)
    print(f"Class {node.name} loaded.")

    void visit_ArrayNode(self, node):
        return [self.visit(element) 
      for element in node.elements]

    void visit_InputNode(self, node):
        return input(">> ")


  void visit_DoWhileNode(self, node):
    while True:
        for stmt in node.body:
            self.visit(stmt)
        if not self.visit(node.condition):
            break
