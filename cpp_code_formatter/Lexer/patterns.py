from Lexer.Automaton.state_machine_factory import *
from Lexer.Token.token import *


PATTERNS = ((whitespace_state_machine(), TokenName.WHITESPACE),
            (separator_state_machine(), TokenName.SEPARATOR),
            (bracket_state_machine(), TokenName.BRACKET),
            (number_state_machine(), TokenName.INT_NUMBER),
            (identifier_state_machine(), TokenName.IDENTIFIER),
            (double_quote_string_state_machine(), TokenName.STRING),
            (char_symbol_state_machine(), TokenName.CHAR_SYMBOL),
            (new_line_state_machine(), TokenName.NEW_LINE))

KEYWORDS = ("for", "if", "else", "do", "while", "break", "switch", "case", "catch", "throw", "const", "continue",
            "default", "delete", "new", "asm", "enum", "explicit", "export", "enter", "true", "false", "friend",
            "goto", "inline", "namespace", "mutable", "operator", "virtual", "override", "register", "return",
            "sizeof", "static", "struct", "template", "this", "try", "union", "using", "volatile", "typedef",
            "typeid", "typename")

DATA_TYPES = ("int", "float", "double", "char", "bool", "unsigned", "signed", "auto", "long", "wchar_t", "size_t")

ACCESS_MODIFIERS = ("private", "protected", "public")