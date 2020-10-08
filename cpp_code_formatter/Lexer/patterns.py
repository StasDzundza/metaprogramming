from Lexer.Automaton.state_machine_factory import *
from Lexer.Token.token import *


PATTERNS = ((whitespace_state_machine(), TokenName.WHITESPACE),
            (r"\".*\"", TokenName.STRING),
            (r"\?", TokenName.TERNARY_OPERATOR),
            ("#", TokenName.PREPROCESSOR),
            (r"/\*(\s|.)*\*/", TokenName.MULTILINE_COMMENT),
            (r"//.*(\r|\n|\r\n|$)", TokenName.SINGLE_LINE_COMMENT),
            (r"[+-]?([0-9]*\.)[0-9]+", TokenName.FLOAT_NUMBER),
            (r"[+-]?[0-9]+", TokenName.INT_NUMBER),
            (operator_state_machine(), TokenName.OPERATOR),
            (comparison_operator_state_machine(), TokenName.OPERATOR),
            (separator_state_machine(), TokenName.SEPARATOR),
            (bracket_state_machine(), TokenName.BRACKET),
            (identifier_state_machine(), TokenName.IDENTIFIER),
            (char_symbol_state_machine(), TokenName.CHAR_SYMBOL),
            (new_line_state_machine(), TokenName.NEW_LINE))

KEYWORDS = ("for", "if", "else", "do", "while", "break", "switch", "case", "catch", "throw", "const", "continue",
            "default", "delete", "new", "asm", "enum", "explicit", "export", "enter", "true", "false", "friend",
            "goto", "inline", "namespace", "mutable", "operator", "virtual", "override", "register", "return",
            "sizeof", "static", "struct", "template", "this", "try", "union", "using", "volatile", "typedef",
            "typeid", "typename")

DATA_TYPES = ("int", "float", "double", "char", "bool", "unsigned", "signed", "auto", "long", "wchar_t", "size_t",
              "void")

ACCESS_MODIFIERS = ("private", "protected", "public")