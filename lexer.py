class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"{self.type}:{self.value}" if self.value else self.type

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def generate_tokens(self):
        tokens = []
        while self.current_char:
            if self.current_char.isspace():
                self.advance()
            elif self.current_char.isdigit():
                tokens.append(self.make_number())
            elif self.current_char.isalpha():
                tokens.append(self.make_identifier())
            elif self.current_char == '"':
                tokens.append(self.make_string())
            elif self.current_char == '=':
                tokens.append(Token(TT_ASSIGN, '='))
                self.advance()
            elif self.current_char == '+':
                tokens.append(Token(TT_OPERATOR, '+'))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            elif self.current_char == '{':
                tokens.append(Token(TT_LBRACE))
                self.advance()
            elif self.current_char == '}':
                tokens.append(Token(TT_RBRACE))
                self.advance()
            else:
                self.advance()
        tokens.append(Token(TT_EOF))
        return tokens

    def make_number(self):
        num_str = ''
        while self.current_char and self.current_char.isdigit():
            num_str += self.current_char
            self.advance()
        return Token(TT_INT, int(num_str))

    def make_string(self):
        self.advance()  # Skip starting quote
        str_val = ''
        while self.current_char and self.current_char != '"':
            str_val += self.current_char
            self.advance()
        self.advance()  # Skip ending quote
        return Token(TT_STRING, str_val)

    def make_identifier(self):
        id_str = ''
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            id_str += self.current_char
            self.advance()
        tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
        return Token(tok_type, id_str)
