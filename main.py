# main.py

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

with open("examples/sample1.nx", "r") as f:
    code = f.read()

lexer = Lexer(code)
tokens = lexer.generate_tokens()

parser = Parser(tokens)
ast = parser.parse()

interpreter = Interpreter()
for stmt in ast:
    interpreter.visit(stmt)

if __name__ == "__main__":
    run_file("sample_program.snl")
