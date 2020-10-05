from Lexer.Automaton.state_machine_factory import *
from Lexer.Token.token import *


PATTERNS = [[bracket_state_machine(), TokenName.BRACKET],
            [separator_state_machine(), TokenName.SEPARATOR]]

KEYWORDS = ("for", "if", "else", "do", "while", "break", "switch", "case", "catch", "throw", "const", "continue",
            "default", "delete", "new", "asm", "enum", "explicit", "export", "enter", "true", "false", "friend",
            "goto", "inline", "namespace", "mutable", "operator", "virtual", "override", "register", "return",
            "sizeof", "static", "struct", "template", "this", "try", "union", "using", "volatile", "typedef",
            "typeid", "typename")

DATA_TYPES = ("int", "float", "double", "char", "bool", "unsigned", "signed", "auto", "long", "wchar_t")

ACCESS_MODIFIERS = ("private", "protected", "public")