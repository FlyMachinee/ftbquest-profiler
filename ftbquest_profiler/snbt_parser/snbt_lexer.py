from io import FileIO
import ply.lex as lex
from ..snbt.basic_type import *


class SNBTLexer:

    def __init__(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def input(self, data):
        self.from_file = False
        self.lexer.input(data)

    def input_file(self, file: FileIO):
        self.from_file = True
        self.file: FileIO = file
        self.lexer.input(file.readline())

    def token(self):
        return self.lexer.token()

    reserved = {
        "I": "I",  # Int array type indicator
        "B": "B",  # Byte array type indicator
        "L": "L",  # Long array type indicator
    }

    tokens = [
        "LC",  # {
        "RC",  # }
        "LB",  # [
        "RB",  # ]
        "COLON",  # :
        "SEMI",  # ;
        "STRING",  # "string" or 'string'
        "BYTE",  # 12b
        "SHORT",  # 12345s
        "INT",  # 123456
        "LONG",  # 1234567890l
        "FLOAT",  # 12.34f
        "DOUBLE",  # 12.34d
        "BOOL",  # true, false
        "ID",  # unquoted identifiers
    ] + list(reserved.values())

    t_LC = r"\{"
    t_RC = r"\}"
    t_LB = r"\["
    t_RB = r"\]"
    t_COLON = r":"
    t_SEMI = r";"

    def t_BYTE(self, t):
        r"-?\d+[bB]"
        t.value = Byte(int(t.value[:-1]))
        return t

    def t_SHORT(self, t):
        r"-?\d+[sS]"
        t.value = Short(int(t.value[:-1]))
        return t

    def t_LONG(self, t):
        r"-?\d+[lL]"
        t.value = Long(int(t.value[:-1]))
        return t

    def t_FLOAT(self, t):
        r"-?\d+\.\d+[fF]"
        t.value = Float(float(t.value[:-1]))
        return t

    def t_DOUBLE(self, t):
        r"-?\d+\.\d+[dD]"
        t.value = Double(float(t.value[:-1]))
        return t

    def t_INT(self, t):
        r"-?\d+"
        t.value = Int(int(t.value))
        return t

    def t_BOOL(self, t):
        r"(true|false)"
        t.value = Boolean(t.value == "true")
        return t

    def t_ID(self, t):
        r"[A-Za-z_][A-Za-z0-9_]*"
        t.type = self.reserved.get(t.value, "ID")
        return t

    def t_STRING(self, t):
        r"(\"([^\\\"]|\\.)*\")|(\'([^\\\']|\\.)*\')"
        t.value = String(t.value[1:-1])
        return t

    def t_newline(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value)

    t_ignore = " \t\r,"

    def t_eof(self, t):
        if self.from_file:
            line = self.file.readline()
            if line:
                self.lexer.input(line)
                return self.lexer.token()
        t.lexer.lineno = 1
        return None

    def t_error(self, t):
        print(
            f"Illegal character '{t.value[0]}' at line {t.lineno}, file {self.file.name if self.from_file else 'string input'}"
        )
        t.lexer.skip(1)
