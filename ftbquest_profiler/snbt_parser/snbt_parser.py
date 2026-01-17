from io import FileIO
import ply.yacc as yacc
from ..snbt import SNBT, SNBTList, SNBTArray
from .snbt_lexer import SNBTLexer


class SNBTParser:
    tokens = SNBTLexer.tokens

    def __init__(self, **kwargs) -> None:
        self.lexer = SNBTLexer()
        self.parser = yacc.yacc(module=self, **kwargs)

    def parse(self, data) -> SNBT:
        self.from_file = False
        self.lexer.input(data)
        return self.parser.parse(lexer=self.lexer.lexer)

    def parse_file(self, file: FileIO) -> SNBT:
        self.from_file = True
        self.file = file
        self.lexer.input_file(file)
        return self.parser.parse(lexer=self.lexer.lexer)

    start = "snbt"

    def p_snbt(self, p):
        """snbt : LC snbt_pair_list RC
        | LC RC"""
        if len(p) == 4:
            p[0] = p[2]
        else:
            p[0] = SNBT()

    def p_snbt_pair_list(self, p):
        """snbt_pair_list   : snbt_pair
        | snbt_pair_list snbt_pair"""
        if len(p) == 2:
            p[0] = SNBT({p[1][0]: p[1][1]})
        else:
            p[0] = p[1]
            key, value = p[2]
            p[0][key] = value

    def p_snbt_pair_id_key(self, p):
        """snbt_pair : ID COLON snbt_value"""
        p[0] = (p[1], p[3])

    def p_snbt_pair_string_key(self, p):
        """snbt_pair : STRING COLON snbt_value"""
        p[0] = (str(p[1])[1:-1], p[3])

    def p_snbt_pair_num_key(self, p):
        """snbt_pair : INT COLON snbt_value"""
        # wtf, why would someone use a number as a key
        p[0] = (str(p[1]), p[3])

    def p_snbt_value(self, p):
        """snbt_value  : STRING
        | BYTE
        | SHORT
        | INT
        | LONG
        | FLOAT
        | DOUBLE
        | BOOL
        | snbt
        | snbt_list
        | snbt_array"""
        p[0] = p[1]

    def p_snbt_list(self, p):
        """snbt_list : LB snbt_list_elements RB
        | LB RB"""
        if len(p) == 4:
            p[0] = p[2]
        else:
            p[0] = SNBTList([])

    def p_snbt_list_elements(self, p):
        """snbt_list_elements   : snbt_value
        | snbt_list_elements snbt_value"""
        if len(p) == 2:
            p[0] = SNBTList([p[1]])
        else:
            p[0] = p[1]
            p[0].append(p[2])

    def p_snbt_array(self, p):
        """snbt_array : LB array_type SEMI snbt_array_elements RB
        | LB array_type SEMI RB"""
        if len(p) == 6:
            p[0] = p[4]
        else:
            p[0] = SNBTArray(self.array_type.lower(), [])
        self.array_type = None
        self.array_min = None
        self.array_max = None

    def p_array_type(self, p):
        """array_type : B
        | I
        | L"""
        p[0] = p[1]
        self.array_type: str = p[1]
        self.array_min: int = {
            "B": -128,
            "I": -2147483648,
            "L": -9223372036854775808,
        }[self.array_type]
        self.array_max: int = {
            "B": 127,
            "I": 2147483647,
            "L": 9223372036854775807,
        }[self.array_type]

    def p_snbt_array_elements(self, p):
        """snbt_array_elements   : snbt_array_element
        | snbt_array_elements snbt_array_element"""
        if self.array_min is None or self.array_max is None:
            raise SyntaxError("Array type not specified before elements")
        if len(p) == 2:
            if not (self.array_min <= p[1] <= self.array_max):
                raise ValueError(
                    f"Array element {p[1]} out of bounds for type {self.array_type}"
                )
            p[0] = SNBTArray(self.array_type.lower(), [p[1]])
        else:
            if not (self.array_min <= p[2] <= self.array_max):
                raise ValueError(
                    f"Array element {p[2]} out of bounds for type {self.array_type}"
                )
            p[0] = p[1]
            p[0].append(p[2])

    def p_snbt_array_element(self, p):
        """snbt_array_element : BYTE
        | INT
        | LONG"""
        p[0] = p[1]

    def p_error(self, p):
        if p:
            raise SyntaxError(
                f"Syntax error at '{p.value}' (line {p.lineno}), file {self.file.name if self.from_file else 'string input'}"
            )
        else:
            raise SyntaxError("Syntax error at EOF")
