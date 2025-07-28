# parser.py

from tokens import *
from ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]

    def parse(self):
        statements = []
        while self.current_token.type != TT_EOF:
            stmt = self.statement()
            if stmt:
                statements.append(stmt)
        return statements

    def statement(self):
        if self.current_token.matches(TT_KEYWORD, "print"):
            return self.print_stmt()
        elif self.current_token.matches(TT_KEYWORD, "def"):
            return self.function_def()
        elif self.current_token.matches(TT_KEYWORD, "if"):
            return self.if_stmt()
        elif self.current_token.matches(TT_KEYWORD, "for"):
            return self.for_loop()
        elif self.current_token.matches(TT_KEYWORD, "while"):
            return self.while_loop()
        elif self.current_token.type == TT_KEYWORD and self.peek().type == TT_IDENTIFIER:
            return self.var_assign()
        elif self.current_token.type == TT_IDENTIFIER:
            return self.var_or_func()
        else:
            self.advance()

    def print_stmt(self):
        self.advance()
        expr = self.expression()
        return PrintNode(expr)

    def var_assign(self):
        var_type = self.current_token.value
        self.advance()
        var_name = self.current_token.value
        self.advance()  # var name
        self.advance()  # =
        expr = self.expression()
        return VarAssignNode(var_name, expr)

    def var_or_func(self):
        identifier = self.current_token.value
        self.advance()
        if self.current_token.type == TT_LPAREN:
            self.advance()
            args = []
            while self.current_token.type != TT_RPAREN:
                args.append(self.expression())
                if self.current_token.type == TT_COMMA:
                    self.advance()
            self.advance()
            return FunctionCallNode(identifier, args)
        else:
            return VarAccessNode(identifier)

    def function_def(self):
        self.advance()
        func_name = self.current_token.value
        self.advance()
        self.advance()  # skip (
        params = []
        while self.current_token.type != TT_RPAREN:
            if self.current_token.type == TT_IDENTIFIER:
                params.append(self.current_token.value)
            self.advance()
        self.advance()  # skip )
        self.advance()  # skip {
        body = []
        while self.current_token.type != TT_RBRACE:
            body.append(self.statement())
        self.advance()  # skip }
        return FunctionDefNode(func_name, params, body)

    def if_stmt(self):
        self.advance()  # skip if
        condition = self.expression()
        self.advance()  # skip {
        then_body = []
        while self.current_token.type != TT_RBRACE:
            then_body.append(self.statement())
        self.advance()
        else_body = []
        if self.current_token.matches(TT_KEYWORD, "else"):
            self.advance()
            self.advance()
            while self.current_token.type != TT_RBRACE:
                else_body.append(self.statement())
            self.advance()
        return IfNode(condition, then_body, else_body)

    def for_loop(self):
        self.advance()
        self.advance()  # skip int
        var_name = self.current_token.value
        self.advance()  # variable name
        self.advance()  # =
        start_val = self.expression()
        self.advance()  # ;
        condition = self.expression()
        self.advance()  # ;
        self.advance()  # i++
        end_val = condition.right_node
        self.advance()  # {
        body = []
        while self.current_token.type != TT_RBRACE:
            body.append(self.statement())
        self.advance()
        return ForNode(var_name, start_val, end_val, body)

    def while_loop(self):
        self.advance()
        condition = self.expression()
        self.advance()  # {
        body = []
        while self.current_token.type != TT_RBRACE:
            body.append(self.statement())
        self.advance()
        return WhileNode(condition, body)

    def expression(self):
        left = self.term()
        while self.current_token.type == TT_OPERATOR:
            op_token = self.current_token
            self.advance()
            right = self.term()
            left = BinOpNode(left, op_token, right)
        return left

    def term(self):
        tok = self.current_token
        if tok.type == TT_INT:
            self.advance()
            return NumberNode(tok.value)
        elif tok.type == TT_STRING:
            self.advance()
            return StringNode(tok.value)
        elif tok.type == TT_IDENTIFIER:
            self.advance()
            return VarAccessNode(tok.value)

    def peek(self):
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return Token(TT_EOF)
