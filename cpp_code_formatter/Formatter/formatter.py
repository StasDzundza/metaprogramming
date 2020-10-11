from Lexer.lexer import *
from Formatter.config import *
from Lexer.patterns import *


class Formatter:
    def __init__(self):
        self.KEYWORDS_WITH_PARENTHESIS = ("if", "for", "while", "switch", "catch")
        self.KEYWORDS_WITH_SPACE_AFTER = ("throw", "const", "new", "delete", "explicit", "export", "friend", "goto",
                                          "inline", "namespace", "mutual", "virtual", "register", "return", "static",
                                          "using", "volatile", "typedef", "class", "struct", "enum", "case")
        self.log_file_name = "log.log"
        self.need_indent = False

    def code_style_error_log(self):  # TODO add logging for code style error
        pass

    def is_space_before_parenthesis(self, keyword):
        if keyword == "if":
            return if_parenthesis
        if keyword == "for":
            return for_parenthesis
        if keyword == "while":
            return while_parenthesis
        if keyword == "switch":
            return switch_parenthesis
        if keyword == "catch":
            return catch_parenthesis
        if keyword == "identifier":
            return func_decl_parenthesis
        return False

    def is_space_before_curly_open_brace(self, keyword):
        if keyword in ("class", "struct"):
            return before_class_struct_left_brace
        if keyword == "namespace":
            return before_ns_left_brace
        if keyword == "if":
            return before_if_left_brace
        if keyword == "else":
            return before_else_left_brace
        if keyword == "for":
            return before_for_left_brace
        if keyword == "while":
            return before_while_left_brace
        if keyword == "do":
            return before_do_left_brace
        if keyword == "switch":
            return before_switch_left_brace
        if keyword == "try":
            return before_try_left_brace
        if keyword == "catch":
            return before_catch_left_brace
        return False

    def is_space_before_keyword(self, keyword):
        if keyword == "else":
            return before_else
        if keyword == "catch":
            return before_catch
        return False

    def add_spaces_around_operator(self, operator):
        if operator in ("=", "+=", "-=", "/=", "*=", "^=", "&=", "^=", "<<=", ">>=", "%="):
            return ' ' + operator + ' ' if around_assignment_op else operator
        if operator in ("&&", "||"):
            return ' ' + operator + ' ' if around_logical_op else operator
        if operator in ("==", "!="):
            return ' ' + operator + ' ' if around_equality_op else operator
        if operator in ("<", "<=", ">", ">=", "!=", "<=>"):
            return ' ' + operator + ' ' if around_relational_op else operator
        if operator in ("&", "^", "|"):
            return ' ' + operator + ' ' if around_bitwise_op else operator
        if operator in ("+", "-"):
            return ' ' + operator + ' ' if around_additive_op else operator
        if operator in (">>", "<<"):
            return ' ' + operator + ' ' if around_shift_op else operator
        if operator in (".", "->", "->*", ".*"):
            return ' ' + operator + ' ' if around_pointer_to_member_op else operator
        return operator

    def add_indent(self, indent_level, output, after=False):
        if self.need_indent:
            indent = ' ' * indent_len * indent_level
            output = (output + indent if after else indent + output)
        return output

    def format_file(self, path_to_code):
        token_stack = []
        output = ""
        lexer = Lexer()
        indent_level = 0
        last_keyword = ''
        tokens = lexer.tokenize(path_to_code)
        for i in range(0, len(tokens)):
            cur_token = tokens[i]
            cur_output = ""
            if cur_token.token_name == TokenName.KEYWORD:
                last_keyword = cur_token.value
                if cur_token.value in self.KEYWORDS_WITH_PARENTHESIS:
                    token_stack.append(cur_token.value)
                    cur_output = (
                        cur_token.value + ' ' if self.is_space_before_parenthesis(cur_token.value) else cur_token.value)
                elif cur_token.value in self.KEYWORDS_WITH_SPACE_AFTER:
                    cur_output = cur_token.value + ' '
                    if cur_token.value == "case":
                        pass
                elif cur_token.value in ("else", "catch"):
                    cur_output = ' ' + cur_token.value if self.is_space_before_keyword(cur_token.value) else cur_token.value
                else:
                    if cur_token.value in ("class", "struct", "enum", "template"):
                        token_stack.append(cur_token.value)
                    cur_output = cur_token.value
                cur_output = self.add_indent(indent_level, cur_output)
                self.need_indent = False
            elif cur_token.token_name == TokenName.IDENTIFIER:
                if (i + 1 < len(tokens) and tokens[i + 1].value == '(') or \
                        (i + 2 < len(tokens) and tokens[i + 1].token_name == TokenName.WHITESPACE and tokens[i + 2].value == '('):
                    token_stack.append("identifier")
                    cur_output = (cur_token.value + ' ' if self.is_space_before_parenthesis("identifier") else cur_token.value)
                    cur_output = self.add_indent(indent_level, cur_output)
                    self.need_indent = False
                else:
                    cur_output = cur_token.value
                    cur_output = self.add_indent(indent_level, cur_output)
                    self.need_indent = False
            elif cur_token.token_name == TokenName.BRACKET:
                if cur_token.value == '{':
                    if len(token_stack) > 0 and token_stack[-1].value == "class":
                        token_stack.pop()
                    cur_output = " {\n" if self.is_space_before_curly_open_brace(last_keyword) else "{\n" # TODO check if need \n and indent ++ after {
                    last_keyword = ''
                    cur_output = self.add_indent(indent_level, cur_output)
                    self.need_indent = True
                    indent_level += 1
                elif cur_token.value == '}':
                    indent_level -= 1
                    if (i + 1 < len(tokens) and tokens[i+1].value in ("else", "catch", ";")) or \
                            (i + 2 < len(tokens) and tokens[i+2].value in ("else", "catch", ";")):
                        cur_output = "}"
                    else:
                        cur_output = "}\n"
                    cur_output = self.add_indent(indent_level, cur_output)
                    self.need_indent = True
                elif cur_token.value == ')':
                    cur_output = ')'
                    if len(token_stack) > 0 and token_stack[-1] == "identifier":
                        token_stack.pop()
                    elif len(token_stack) > 0 and token_stack[-1] in self.KEYWORDS_WITH_PARENTHESIS:
                        if (i+2 < len(tokens) and tokens[i+1].token_name in (TokenName.WHITESPACE, TokenName.NEW_LINE) and tokens[i+2].value == '{') or \
                             (i+1 < len(tokens) and tokens[i+1].value == '{'):
                            pass
                        else:
                            cur_output = cur_output + '\n' + (' ' * indent_len * (indent_level + 1))
                        token_stack.pop()
                    self.need_indent = False
                else:
                    cur_output = cur_token.value
                    cur_output = self.add_indent(indent_level, cur_output)
                    self.need_indent = False
            elif cur_token.token_name == TokenName.SEPARATOR:
                if cur_token.value == ';':
                    if len(token_stack) > 0 and token_stack[-1] == "for":
                        cur_output = ';'  # TODO check for spaces near ;
                    else:
                        last_keyword = ''
                        cur_output = ';\n'
                        self.need_indent = True
                elif cur_token.value == ':':
                    if len(token_stack) > 0 and token_stack[-1] == '?':
                        token_stack.pop()
                        cur_output = ' :' if before_colon_ternary else ':'
                        cur_output = cur_output + (' ' if after_colon_ternary else '')
                    elif len(token_stack) > 0 and token_stack[-1] in ACCESS_MODIFIERS:
                        token_stack.pop()
                        cur_output = ":\n"
                        self.need_indent = True
                    elif len(token_stack) > 0 and (token_stack[-1] == "case" or token_stack[-1] == "default"):
                        token_stack.pop()
                        cur_output = ":\n"
                        indent_level += 1
                        self.need_indent = True
                    else:
                        cur_output = cur_token.value
                else:
                    cur_output = cur_token.value
            elif cur_token.token_name == TokenName.DATA_TYPE:
                cur_output = cur_token.value + ' '
                cur_output = self.add_indent(indent_level, cur_output)
                self.need_indent = False
            elif cur_token.token_name == TokenName.OPERATOR:
                if len(token_stack) > 0 and token_stack[-1] == "include" and cur_token.value in ('<', '>'):
                    cur_output = ('<' if cur_token.value == '<' else '>')
                else:
                    cur_output = self.add_spaces_around_operator(cur_token.value)
                    cur_output = self.add_indent(indent_level, cur_output)
                    self.need_indent = False
            elif cur_token.token_name == TokenName.PREPROCESSOR_DIRECTIVE:
                token_stack.append(cur_token.value)
                cur_output = cur_token.value + ' '
            elif cur_token.token_name == TokenName.TERNARY_OPERATOR:
                token_stack.append('?')
                cur_output = ' ?' if before_ternary else '?'
                cur_output = cur_output + (' ' if after_ternary else '')
            elif cur_token.token_name == TokenName.ACCESS_MODIFIER:
                if (i+1 < len(tokens) and tokens[i+1].token_name == TokenName.IDENTIFIER) or \
                    (i+2 < len(tokens) and tokens[i+1].token_name == TokenName.WHITESPACE and tokens[i+2].token_name == TokenName.IDENTIFIER):
                    cur_output = cur_token.value + ' '
                else:
                    token_stack.append(cur_token.value)
                    cur_output = cur_token.value
            elif cur_token.token_name == TokenName.WHITESPACE:
                pass
            elif cur_token.token_name == TokenName.NEW_LINE:
                if len(token_stack) > 0 and token_stack[-1] in PREPROCESSOR_DIRECTIVES:
                    cur_output = '\n'
                    token_stack.pop()
            else:
                cur_output = cur_token.value
                cur_output = self.add_indent(indent_level, cur_output)
                self.need_indent = False

            output = output + cur_output

        return output

    def format_files_in_dir(self, dir_path):
        pass