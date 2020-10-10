from Lexer.lexer import *
from Lexer.Token.token import *
from Formatter.config import *


class Formatter():
    def __init__(self):
        self.KEYWORDS_WITH_PARENTHESIS = ("if", "for", "while", "switch", "catch")
        self.log_file_name = "log.log"

    def code_style_error_log(self):  # TODO add logging for code style error
        pass

    def is_space_before_parenthesis(self, keyword):
        if keyword == "if":
            if if_parenthesis:
                return True
            else:
                return False
        if keyword == "for":
            if for_parenthesis:
                return True
            else:
                return False
        if keyword == "while":
            if while_parenthesis:
                return True
            else:
                return False
        if keyword == "switch":
            if switch_parenthesis:
                return True
            else:
                return False
        if keyword == "catch":
            if catch_parenthesis:
                return True
            else:
                return False
        if keyword == "identifier":
            if func_decl_parenthesis:
                return True
            else:
                return False
        return False

    def format_file(self, path_to_code):
        token_stack = []
        output = ""
        lexer = Lexer()
        tokens = lexer.tokenize(path_to_code)
        for i in range(0, len(tokens)):
            cur_token = tokens[i]
            cur_output = ""
            if cur_token.token_name == TokenName.KEYWORD:
                if cur_token.value in self.KEYWORDS_WITH_PARENTHESIS:
                    token_stack.append(cur_token.value)
                    cur_output = (cur_token.value + ' ' if self.is_space_before_parenthesis(cur_token.value) else cur_token.value)
                else:
                    pass
            elif cur_token.token_name == TokenName.IDENTIFIER:
                if i + 1 < len(tokens) and tokens[i + 1].value == '(':
                    cur_output = (cur_token.value + ' ' if self.is_space_before_parenthesis("identifier") else cur_token.value)
                else:
                    cur_output = cur_token.value
            else:
                cur_output = cur_token.value

            output = output + cur_output

        return output
