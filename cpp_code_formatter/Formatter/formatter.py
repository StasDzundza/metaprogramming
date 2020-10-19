from Lexer.lexer import *
from Lexer.patterns import *
import os
import json


class Formatter:
    def __init__(self):
        self.KEYWORDS_WITH_PARENTHESIS = ("if", "for", "while", "switch", "catch")
        self.KEYWORDS_WITH_SPACE_AFTER = ("throw", "const", "new", "delete", "explicit", "export", "friend", "goto",
                                          "inline", "namespace", "mutual", "virtual", "register", "return", "static",
                                          "using", "volatile", "typedef", "class", "struct", "enum", "case", "typename")
        self.log_file_name = "log.log"
        self.need_indent = False
        self.config_file_path = "config.json"
        self.c = self.configure_formatter(self.config_file_path)

    def is_space_before_parenthesis(self, keyword):
        if keyword == "if":
            return True if self.c["if_parenthesis"] == 1 else False
        if keyword == "for":
            return True if self.c["for_parenthesis"] == 1 else False
        if keyword == "while":
            return True if self.c["while_parenthesis"] == 1 else False
        if keyword == "switch":
            return True if self.c["switch_parenthesis"] == 1 else False
        if keyword == "catch":
            return True if self.c["catch_parenthesis"] == 1 else False
        if keyword == "identifier":
            return True if self.c["func_decl_parenthesis"] == 1 else False
        return False

    def is_space_before_curly_open_brace(self, keyword):
        if keyword in ("class", "struct"):
            return True if self.c["before_class_struct_left_brace"] == 1 else False
        if keyword == "namespace":
            return True if self.c["before_ns_left_brace"] == 1 else False
        if keyword == "if":
            return True if self.c["before_if_left_brace"] == 1 else False
        if keyword == "else":
            return True if self.c["before_else_left_brace"] == 1 else False
        if keyword == "for":
            return True if self.c["before_for_left_brace"] == 1 else False
        if keyword == "while":
            return True if self.c["before_while_left_brace"] == 1 else False
        if keyword == "do":
            return True if self.c["before_do_left_brace"] == 1 else False
        if keyword == "switch":
            return True if self.c["before_switch_left_brace"] == 1 else False
        if keyword == "try":
            return True if self.c["before_try_left_brace"] == 1 else False
        if keyword == "catch":
            return True if self.c["before_catch_left_brace"] == 1 else False
        return False

    def is_space_before_keyword(self, keyword):
        if keyword == "else":
            return True if self.c["before_else"] == 1 else False
        if keyword == "catch":
            return True if self.c["before_catch"] == 1 else False
        return False

    def add_spaces_around_operator(self, operator):
        if operator in ("=", "+=", "-=", "/=", "*=", "^=", "&=", "^=", "<<=", ">>=", "%="):
            return ' ' + operator + ' ' if self.c["around_assignment_op"] == 1 else operator
        if operator in ("&&", "||"):
            return ' ' + operator + ' ' if self.c["around_logical_op"] == 1 else operator
        if operator in ("==", "!="):
            return ' ' + operator + ' ' if self.c["around_equality_op"] == 1 else operator
        if operator in ("<", "<=", ">", ">=", "!=", "<=>"):
            return ' ' + operator + ' ' if self.c["around_relational_op"] == 1 else operator
        if operator in ("&", "^", "|"):
            return ' ' + operator + ' ' if self.c["around_bitwise_op"] == 1 else operator
        if operator in ("+", "-"):
            return ' ' + operator + ' ' if self.c["around_additive_op"] == 1 else operator
        if operator in (">>", "<<"):
            return ' ' + operator + ' ' if self.c["around_shift_op"] == 1 else operator
        if operator in (".", "->", "->*", ".*"):
            return ' ' + operator + ' ' if self.c["around_pointer_to_member_op"] == 1 else operator
        return operator

    def add_indent(self, indent_level, output, after=False):
        if self.need_indent:
            indent = ' ' * self.c["indent_len"]\
                     * indent_level
            output = (output + indent if after else indent + output)
        return output

    def is_space_within_parenthesis(self, keyword):
        if keyword == "for":
            return True if self.c["within_for"] == 1 else False
        if keyword == "if":
            return True if self.c["within_if"] == 1 else False
        if keyword == "switch":
            return True if self.c["within_switch"] == 1 else False
        if keyword == "catch":
            return True if self.c["within_catch"] == 1 else False
        if keyword == "while":
            return True if self.c["within_while"] == 1 else False
        return False

    def format_file(self, path_to_code):
        token_stack = []
        output = ""
        lexer = Lexer()
        indent_level = 0
        last_keyword = ''
        first_case = True
        with open(path_to_code, 'r', encoding="utf-8") as file:
            tokens = lexer.tokenize(file.read())
        for i in range(0, len(tokens)):
            cur_token = tokens[i]
            cur_output = ""
            if cur_token.token_name == TokenName.KEYWORD:
                last_keyword = cur_token.value
                if cur_token.value in ("class", "struct", "enum", "template"):
                    token_stack.append(cur_token.value)
                    if cur_token.value == "class" and "template" in token_stack:
                        token_stack.pop()  # if class instead typename in template
                if cur_token.value in self.KEYWORDS_WITH_PARENTHESIS:
                    token_stack.append(cur_token.value)
                    cur_output = (
                        cur_token.value + ' ' if self.is_space_before_parenthesis(cur_token.value) else cur_token.value)
                    if cur_token.value == "switch":
                        first_case = True
                elif cur_token.value in self.KEYWORDS_WITH_SPACE_AFTER:
                    cur_output = cur_token.value + ' '
                elif cur_token.value in ("else", "catch"):
                    cur_output = ' ' + cur_token.value if self.is_space_before_keyword(
                        cur_token.value) else cur_token.value
                elif cur_token.value == "operator":
                    cur_output = "operator " if self.c["between_operator_keyword_and_punctuation"] == 1 else "operator"
                else:
                    cur_output = cur_token.value
                if cur_token.value in ("case", "default"):
                    token_stack.append(cur_token.value)
                    if first_case:
                        first_case = False
                    else:
                        indent_level -= 1
                cur_output = self.add_indent(indent_level, cur_output)
                self.need_indent = False
            elif cur_token.token_name == TokenName.IDENTIFIER:
                if (i + 1 < len(tokens) and tokens[i + 1].value in ('(', '{')) or \
                        (i + 2 < len(tokens) and tokens[i + 1].token_name == TokenName.WHITESPACE and tokens[
                            i + 2].value in ('(', '{')):
                    token_stack.append("identifier")
                    cur_output = (
                        cur_token.value + ' ' if self.is_space_before_parenthesis("identifier") else cur_token.value)
                else:
                    cur_output = cur_token.value
                cur_output = self.add_indent(indent_level, cur_output)
                self.need_indent = False
            elif cur_token.token_name == TokenName.BRACKET:
                if cur_token.value == '{':
                    if len(token_stack) > 0 and token_stack[-1] == "identifier":  # initialization
                        cur_output = ' {' if self.c["before_init_list_left_brace"] == 1 else '{'
                        cur_output = cur_output + (' ' if self.c["within_initializer_list_braces"] == 1 else '')
                        if last_keyword != '':
                            cur_output = cur_output + '\n'
                            self.need_indent = True
                            indent_level += 1
                            last_keyword = ''
                            token_stack.pop()  # remove unnecessary identifier
                    else:
                        cur_output = " {\n" if self.is_space_before_curly_open_brace(last_keyword) else "{\n"
                        last_keyword = ''
                        cur_output = self.add_indent(indent_level, cur_output)
                        self.need_indent = True
                        indent_level += 1
                    token_stack.append('{')
                elif cur_token.value == '}':
                    if indent_level > 0 and ((len(token_stack) > 1 and token_stack[-2] != "identifier") or len(token_stack) == 1):
                        indent_level -= 1
                    if (i + 1 < len(tokens) and tokens[i + 1].value in ("else", "catch", ";")) or \
                            (i + 2 < len(tokens) and tokens[i + 2].value in ("else", "catch", ";")):
                        cur_output = "}"
                    else:
                        if len(token_stack) > 1 and token_stack[-2] == "identifier":
                            cur_output = ' }' if self.c["within_initializer_list_braces"] == 1 else '}'
                            self.need_indent = False
                        else:
                            cur_output = "}\n"
                    if len(token_stack) > 1 and token_stack[-2] == "switch":
                        indent_level -= 1
                    cur_output = self.add_indent(indent_level, cur_output)
                    self.need_indent = True
                    if len(token_stack) > 0:
                        token_stack.pop()  # remove { from stack
                        if len(token_stack) > 0 and (token_stack[-1] in KEYWORDS or token_stack[-1] == "identifier"):
                            if token_stack[-1] == "identifier":
                                self.need_indent = False
                            token_stack.pop()  # remove keyword like: identifier if for class ...
                elif cur_token.value == ')':
                    cur_output = ' )' if self.is_space_within_parenthesis(last_keyword) else ')'
                    if len(token_stack) > 0 and token_stack[-1] == "identifier":
                        token_stack.pop()
                    elif len(token_stack) > 0 and token_stack[-1] in self.KEYWORDS_WITH_PARENTHESIS:
                        if (i + 2 < len(tokens) and tokens[i + 1].token_name in (
                        TokenName.WHITESPACE, TokenName.NEW_LINE) and tokens[i + 2].value == '{') or \
                                (i + 1 < len(tokens) and tokens[i + 1].value == '{'):
                            pass
                        else:
                            token_stack.pop()
                            cur_output = cur_output + '\n' + (' ' * self.c["indent_len"] * (indent_level + 1))
                    self.need_indent = False
                elif cur_token.value == '(':
                    cur_output = '( ' if self.is_space_within_parenthesis(last_keyword) else '('
                    cur_output = self.add_indent(indent_level, cur_output)
                    self.need_indent = False
                elif cur_token.value == '[':
                    cur_output = '[ ' if self.c["within_array_brackets"] == 1 else '['
                elif cur_token.value == ']':
                    cur_output = ' ]' if self.c["within_array_brackets"] == 1 else ']'
                else:
                    cur_output = cur_token.value
                    cur_output = self.add_indent(indent_level, cur_output)
                    self.need_indent = False
            elif cur_token.token_name == TokenName.SEPARATOR:
                if cur_token.value == ';':
                    if len(token_stack) > 0 and token_stack[-1] == "for":
                        cur_output = ' ;' if self.c["before_for_semicolon"] == 1 else ';'
                        cur_output = cur_output + ' ' if self.c["after_for_semicolon"] == 1 else ''
                    else:
                        last_keyword = ''
                        cur_output = ';\n'
                        self.need_indent = True
                elif cur_token.value == ':':
                    if len(token_stack) > 0 and token_stack[-1] == '?':
                        token_stack.pop()
                        cur_output = ' :' if self.c["before_colon_ternary"] == 1 else ':'
                        cur_output = cur_output + (' ' if self.c["after_colon_ternary"] == 1 else '')
                    elif len(token_stack) > 0 and token_stack[-1] in ACCESS_MODIFIERS:
                        token_stack.pop()
                        cur_output = ":\n"
                        self.need_indent = True
                    elif len(token_stack) > 0 and (token_stack[-1] in ("case", "default")):
                        token_stack.pop()
                        cur_output = ":\n"
                        indent_level += 1
                        self.need_indent = True
                    else:
                        cur_output = ' :' if self.c["before_colon_in_bit_field"] == 1 else ':'
                        cur_output = cur_output + (' ' if self.c["after_colon_in_bit_field"] == 1 else '')
                elif cur_token.value == ',':
                    cur_output = ' ,' if self.c["before_coma"] == 1 else ','
                    cur_output = cur_output + ' ' if self.c["after_coma"] == 1 else ''
                else:
                    cur_output = cur_token.value
            elif cur_token.token_name == TokenName.DATA_TYPE:
                cur_output = cur_token.value + ' '
                cur_output = self.add_indent(indent_level, cur_output)
                self.need_indent = False
            elif cur_token.token_name == TokenName.OPERATOR:
                if len(token_stack) > 0 and token_stack[-1] == "include" and cur_token.value in ('<', '>'):
                    cur_output = ('<' if cur_token.value == '<' else '>')
                elif cur_token.value == '<' and len(token_stack) > 0 and token_stack[-1] == "template":
                    token_stack.append('<')
                    cur_output = " <" if self.c["before_template_declaration"] == 1 else '<'
                    cur_output = cur_output + (' ' if self.c["within_template_declaration"] == 1 else '')
                elif cur_token.value == '>' and len(token_stack) > 0 and token_stack[-1] == '<':
                    token_stack.pop()  # < pop
                    cur_output = " >" if self.c["within_template_declaration"] == 1 else '>'
                    if self.c["within_template_declaration"] == 0 and self.c["prevent_concatenation_in_template"] == 1 and \
                            output[len(output) - 1] == '>':
                        cur_output = ' ' + cur_output
                    if len(token_stack) > 0 and token_stack[-1] == 'template':
                        cur_output = cur_output + '\n'
                        token_stack.pop()  # template pop
                elif cur_token.value == '<' and len(token_stack) > 0 and "template" in token_stack:
                    token_stack.append('<')
                    cur_output = '<'
                elif cur_token.value == '!':
                    cur_output = '! ' if self.c["around_unary_op"] else '!'
                else:
                    cur_output = self.add_spaces_around_operator(cur_token.value)
                self.need_indent = False
            elif cur_token.token_name == TokenName.PREPROCESSOR_DIRECTIVE:
                token_stack.append(cur_token.value)
                cur_output = cur_token.value + ' '
                self.need_indent = True
                cur_output = self.add_indent(self.c["preprocessor_directive_indent"], cur_output)
                self.need_indent = False
            elif cur_token.token_name == TokenName.TERNARY_OPERATOR:
                token_stack.append('?')
                cur_output = ' ?' if self.c["before_ternary"] == 1 else '?'
                cur_output = cur_output + (' ' if self.c["after_ternary"] == 1 else '')
            elif cur_token.token_name == TokenName.ACCESS_MODIFIER:
                if (i + 1 < len(tokens) and tokens[i + 1].token_name == TokenName.IDENTIFIER) or \
                        (i + 2 < len(tokens) and tokens[i + 1].token_name == TokenName.WHITESPACE and tokens[
                            i + 2].token_name == TokenName.IDENTIFIER):
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

        l1 = Lexer()
        l2 = Lexer()
        with open(path_to_code, 'r', encoding="utf-8") as file:
            old = l1.tokenize(file.read())
        new = l2.tokenize(output)
        self.verify(old, new)
        return output

    def format_files_in_project(self, dir_path):
        files = []
        tree = os.walk(dir_path)
        for d in tree:
            cur_dir_name = d[0]
            cur_dir_files = d[2]
            for file in cur_dir_files:
                if file.endswith(".cpp") or file.endswith(".h"):
                    files.append(cur_dir_name + '/' + file)
        for file in files:
            print("#######" + file + "#######")
            formatted_code = self.format_file(file)
            self.save_formatted_file(formatted_code, file)

    def format_files_in_dir(self, dir_path):
        files = []
        tree = os.walk(dir_path)
        for d in tree:
            cur_dir_name = d[0]
            cur_dir_files = d[2]
            for file in cur_dir_files:
                if file.endswith(".cpp") or file.endswith(".h"):
                    files.append(cur_dir_name + '/' + file)
            break
        for file in files:
            print("#######" + file + "#######")
            formatted_code = self.format_file(file)
            self.save_formatted_file(formatted_code, file)

    def format_single_file(self, file_path):
        formatted_code = self.format_file(file_path)
        self.save_formatted_file(formatted_code, file_path)

    def save_formatted_file(self, formatted_code, file_path):
        if file_path.endswith(".cpp"):
            file_path = file_path[:-4]
            file_path = file_path + "_formatted.cpp"
            with open(file_path, 'w') as file:
                file.write(formatted_code)
        elif file_path.endswith(".h"):
            file_path = file_path[:-2]
            file_path = file_path + "_formatted.h"
            with open(file_path, 'w') as file:
                file.write(formatted_code)

    def show_help(self):
        with open("Readme.md", 'r', encoding="utf-8") as file:
            print(file.read())

    def verify_file(self, file_path):
        logs = file_path + '\n\n'
        lexer = Lexer()
        lexer2 = Lexer()
        with open(file_path, 'r', encoding="utf-8") as start_file:
            not_formatted_tokens = lexer.tokenize(start_file.read())
        formatted_code = self.format_file(file_path)
        formatted_tokens = lexer2.tokenize(formatted_code)
        not_formatted_tokens = self.remove_whitespace_tokens(not_formatted_tokens)
        formatted_tokens = self.remove_whitespace_tokens(formatted_tokens)
        for i in range(0, len(formatted_tokens) - 1):
            cur_log = ''
            if not_formatted_tokens[i].line != formatted_tokens[i].line or not_formatted_tokens[i].column != formatted_tokens[i].column:
                cur_log = "ERROR at line " + str(not_formatted_tokens[i].line) + ", column " + str(not_formatted_tokens[i].column) + \
                    ". Current token (" + not_formatted_tokens[i].value + ") should be at line " + str(formatted_tokens[i].line) + \
                    ", column " + str(formatted_tokens[i].column) + '\n\n'
            logs = logs + cur_log
            print(logs)
        with open(self.log_file_name, 'a', encoding="utf-8") as file:
            file.write(logs)

    def remove_whitespace_tokens(self, tokens):
        new_tokens = []
        for token in tokens:
            if token.token_name not in (TokenName.WHITESPACE, TokenName.NEW_LINE):
                new_tokens.append(token)
        return new_tokens

    def configure_formatter(self, config_file_path):
        self.config_file_path = config_file_path
        with open(config_file_path, 'r', encoding="utf-8") as file:
            config = file.read()
            self.c = json.loads(config)
        return self.c

    def verify(self, old_tokens, new_tokens):
        logs = ""
        old_tokens = self.remove_whitespace_tokens(old_tokens)
        new_tokens = self.remove_whitespace_tokens(new_tokens)
        for i in range(0, len(new_tokens) - 1):
            cur_log = ''
            if old_tokens[i].line != new_tokens[i].line or old_tokens[i].column != new_tokens[i].column:
                cur_log = "ERROR at line " + str(old_tokens[i].line) + ", column " + str(old_tokens[i].column) + \
                    ". Current token (" + old_tokens[i].value + ") should be at line " + str(new_tokens[i].line) + \
                    ", column " + str(new_tokens[i].column) + '\n\n'
            logs = logs + cur_log
        with open(self.log_file_name, 'a', encoding="utf-8") as file:
            file.write(logs)

