from enum import Enum


class TokenName(Enum):
    WHITESPACE = 0  # \t, space, ......
    INDENT = 1
    DEDENT = 2
    NEW_LINE = 3
    COMMENT = 4  # //
    OPERATOR = 5  # +, -, *, /, &, |, ^, =, +=, -=, %=, *=, /=, &=, |=, ^=, ~, <<, >>, %
    COMPARISON_OPERATOR = 6  # <, <=, >, >=, ==, !=
    DATA_TYPE = 7  # int, float, complex, str, bool
    KEYWORD = 8
    SEPARATOR = 9  # , ;:
    BRACKET = 10  # (,), [, ], {,}
    DOT = 11  # .
    IDENTIFIER = 12
    NUMBER = 13
    STRING = 14
    MULTILINE_STRING = 15
    ERROR_TOKEN = 16
    NOT_ENDED_MULTILINE_STRING_ERROR = 17
    TERNARY_OPERATOR = 18  # ?


class Token:
    def __init__(self, token_name, value=None):
        self.token_name = token_name
        self.value = value

    def to_string(self):
        if self.value is not None:
            return "{" + self.token_name.name + " | " + self.value + "}"
