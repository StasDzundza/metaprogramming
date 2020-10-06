from enum import Enum


class TokenName(Enum):
    WHITESPACE = 0  # \t, space, ......                                                                    # Done
    NEW_LINE = 1
    OPERATOR = 2  # +, -, *, /, &, |, ^, =, +=, -=, %=, *=, /=, &=, |=, ^=, ~, <<, >>, %
    COMPARISON_OPERATOR = 3  # <, <=, >, >=, ==, !=
    DATA_TYPE = 4                                                                                          # Done
    KEYWORD = 5                                                                                            # Done
    SEPARATOR = 6  # , ;:                                                                                  # Done
    BRACKET = 7  # (,), [, ], {,}                                                                          # Done
    DOT = 8  # .
    IDENTIFIER = 9                                                                                         # Done
    INT_NUMBER = 10
    STRING = 11                                                                                            # Done
    MULTILINE_STRING = 12
    ERROR_TOKEN = 13                                                                                       # Done
    NOT_ENDED_MULTILINE_STRING_ERROR = 14
    TERNARY_OPERATOR = 15  # ?
    COMMENT = 16  # //
    CHAR_SYMBOL = 17                                                                                       # Done
    FLOAT_NUMBER = 18
    ACCESS_MODIFIER = 19                                                                                   # Done


class Token:
    def __init__(self, token_name, value=None):
        self.token_name = token_name
        self.value = value

    def to_string(self):
        if self.value is not None:
            return "{" + self.token_name.name + " | " + self.value + "}"
