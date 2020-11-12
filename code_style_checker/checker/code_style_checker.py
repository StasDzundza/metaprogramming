import os
from utils.logger import *
from lexer.lexer import *
from checker.name_formatter import *
from WorkingMode import *


class ErrorType(Enum):
    TypeNameError = 0,
    ClassMemberNameError = 1,
    FunctionNameError = 2,
    EnumMemberNameError = 3,
    MacrosNameError = 4,
    FileNameError = 5,
    ConstVarError = 6,
    NamespaceNameError = 7,
    CommonVarNameError = 8


class CodeStyleChecker:
    def __init__(self):
        self.mode = "-f"
        self.logger = Logger("code_style_fixing.log", "code_style_verification.log")
        self.user_type_keywords = {"class", "struct", "enum"}

    def fix_code_style(self, file_path, working_mode: WorkingMode):
        lexer = Lexer()
        with open(file_path, 'r', encoding="utf-8") as file:
            cpp_code = file.read()
        tokens = lexer.tokenize(cpp_code)
        token_stack = []
        defined_type_names = []
        defined_functions = []
        defined_namespaces = []
        output = ""
        i = 0
        while i < len(tokens):
            cur_token = tokens[i]
            cur_output = ""
            if cur_token.token_name == TokenName.IDENTIFIER:
                if i + 1 < len(tokens) and tokens[i + 1].value == "::":  # namespace or type names before ::
                    if cur_token.value in defined_namespaces or self.mode != '-f':
                        cur_output = format_common_var_name(cur_token.value)
                        self.log_if_need(file_path, cur_token, cur_output, ErrorType.NamespaceNameError, working_mode)
                    elif cur_token in defined_type_names or self.mode != '-f':
                        cur_output = format_type_name(cur_token.value)
                        self.log_if_need(file_path, cur_token, cur_output, ErrorType.TypeNameError, working_mode)
                    else:
                        cur_output = cur_token.value
                elif len(token_stack) > 0 and token_stack[-1] == "define":  # macro
                    token_stack.pop()  # remove define from stack
                    cur_output = format_macro_name(cur_token.value)
                    self.log_if_need(file_path, cur_token, cur_output, ErrorType.MacrosNameError, working_mode)
                elif i + 1 < len(tokens) and tokens[i + 1].value == '(':  # function
                    prev_token = self.get_prev_token(tokens, i)
                    if prev_token is not None and (
                            prev_token.token_name in (TokenName.DATA_TYPE, TokenName.IDENTIFIER) or
                            prev_token.value in ('*', '&')):  # func declaration
                        defined_functions.append(cur_token.value)
                        cur_output = format_func_name(cur_token.value)
                        self.log_if_need(file_path, cur_token, cur_output, ErrorType.FunctionNameError, working_mode)
                    else:  # func invocation
                        if cur_token.value in defined_functions or self.mode != '-f':
                            cur_output = format_func_name(cur_token.value)
                            self.log_if_need(file_path, cur_token, cur_output, ErrorType.FunctionNameError, working_mode)
                        else:
                            cur_output = cur_token.value  # defined in other file
                elif len(token_stack) > 0 and token_stack[-1] in ("class", "struct", "enum", "typename"):
                    # class,struct,enum, template definition
                    defined_type_names.append(cur_token.value)
                    cur_output = format_type_name(cur_token.value)
                    self.log_if_need(file_path, cur_token, cur_output, ErrorType.TypeNameError, working_mode)
                elif len(token_stack) > 0 and token_stack[-1] in ACCESS_MODIFIERS:  # inheritance
                    token_stack.pop()  # remove access modifier from stack
                    if cur_token.value in defined_type_names or self.mode != '-f':
                        cur_output = format_type_name(cur_token.value)
                        self.log_if_need(file_path, cur_token, cur_output, ErrorType.TypeNameError, working_mode)
                    else:
                        cur_output = cur_token.value
                elif len(token_stack) > 1 and token_stack[-2] == "class":  # class member TODO check for func decl
                    prev_token = self.get_prev_token(tokens, i)
                    if prev_token is not None and (prev_token.token_name in (TokenName.IDENTIFIER, TokenName.DATA_TYPE)
                                                   or prev_token.value in ('*', ',', '&')):
                        cur_output = format_class_var_name(cur_token.value)
                        self.log_if_need(file_path, cur_token, cur_output, ErrorType.ClassMemberNameError, working_mode)
                    else:
                        cur_output = cur_token.value
                elif len(token_stack) > 1 and token_stack[-2] == "enum":  # enum member
                    cur_output = format_const_var_name(cur_token.value)
                    self.log_if_need(file_path, cur_token, cur_output, ErrorType.EnumMemberNameError, working_mode)
                elif len(token_stack) > 0 and token_stack[-1] == "namespace":
                    defined_namespaces.append(cur_token.value)
                    cur_output = format_common_var_name(cur_token.value)
                    self.log_if_need(file_path, cur_token, cur_output, ErrorType.NamespaceNameError, working_mode)
                else:
                    cur_output = cur_token.value
            elif cur_token.token_name == TokenName.KEYWORD:
                if cur_token.value in ("enum", "struct", "namespace", "typename"):
                    token_stack.append(cur_token.value)
                elif cur_token.value == "class":
                    if len(token_stack) > 0 and token_stack[-1] == "enum":  # enum class situation
                        pass
                    else:
                        token_stack.append(cur_token.value)
                cur_output = cur_token.value
            elif cur_token.token_name == TokenName.BRACKET:
                if cur_token.value == "{":
                    token_stack.append("{")
                elif cur_token.value == "}":
                    token_stack.pop()
                    if len(token_stack) > 0 and token_stack[-1] in ("class", "struct", "enum", "namespace"):
                        token_stack.pop()  # remove keyword from stack
                cur_output = cur_token.value
            elif cur_token.token_name == TokenName.ACCESS_MODIFIER:
                token_stack.append(cur_token.value)
                cur_output = cur_token.value
            elif cur_token.token_name == TokenName.SEPARATOR:
                if cur_token.value == ":":
                    if len(token_stack) > 0 and token_stack[-1] in ACCESS_MODIFIERS:
                        token_stack.pop()  # remove access modifier from stack
                cur_output = cur_token.value
            elif cur_token.token_name == TokenName.PREPROCESSOR_DIRECTIVE:
                if cur_token.value in ("include", "define"):
                    token_stack.append(cur_token.value)
                cur_output = cur_token.value
            elif cur_token.token_name == TokenName.STRING:
                if len(token_stack) > 0 and token_stack[-1] == "include":
                    token_stack.pop()
                    if self.mode != "-f":
                        file_name = cur_token.value[1:-1]
                        cur_output = "\"" + format_file_name(file_name) + "\""
                    else:
                        cur_output = cur_token.value
                else:
                    cur_output = cur_token.value
            elif cur_token.token_name == TokenName.COMPARISON_OPERATOR:
                if cur_token.value == '<':  # include, template
                    if len(token_stack) > 0 and token_stack[-1] == "include":
                        token_stack.pop()
                    #  token_stack.append('<')
                elif cur_token.value == '>':
                    pass
                cur_output = cur_token.value
            else:
                cur_output = cur_token.value
            if working_mode == WorkingMode.VerifyMode:
                cur_output = cur_token.value
            output = output + cur_output
            i += 1
        if working_mode == WorkingMode.FixMode:
            # formatted_file_name = os.path.basename(file_path)
            # if self.mode != '-f':
            formatted_file_name = format_file_name(os.path.basename(file_path))
            dir_name = os.path.dirname(file_path)
            self.save_text_in_file(os.path.join(dir_name, formatted_file_name), output)

    def log_if_need(self, file_path, cur_token, cur_output, error_type, mode):
        if cur_output != cur_token.value:
            if error_type == ErrorType.NamespaceNameError:
                self.logger.log(file_path, cur_token.line,
                                "fixed namespace name {} to {}".format(cur_token.value, cur_output), error_type,
                                "Incorrect namespace name", mode)
            elif error_type == ErrorType.ClassMemberNameError:
                self.logger.log(file_path, cur_token.line,
                                "fixed class member name {} to {}".format(cur_token.value, cur_output), error_type,
                                "Incorrect class member name", mode)
            elif error_type == ErrorType.ConstVarError:
                self.logger.log(file_path, cur_token.line,
                                "fixed const var name {} to {}".format(cur_token.value, cur_output), error_type,
                                "Incorrect const var name", mode)
            elif error_type == ErrorType.EnumMemberNameError:
                self.logger.log(file_path, cur_token.line,
                                "fixed enum member name {} to {}".format(cur_token.value, cur_output), error_type,
                                "Incorrect enum member name", mode)
            elif error_type == ErrorType.FileNameError:
                self.logger.log(file_path, cur_token.line,
                                "fixed file name {} to {}".format(cur_token.value, cur_output), error_type,
                                "Incorrect file name", mode)
            elif error_type == ErrorType.FunctionNameError:
                self.logger.log(file_path, cur_token.line,
                                "fixed func name {} to {}".format(cur_token.value, cur_output), error_type,
                                "Incorrect func name", mode)
            elif error_type == ErrorType.TypeNameError:
                self.logger.log(file_path, cur_token.line,
                                "fixed type name {} to {}".format(cur_token.value, cur_output), error_type,
                                "Incorrect type name", mode)
            elif error_type == ErrorType.MacrosNameError:
                self.logger.log(file_path, cur_token.line,
                                "fixed macro name {} to {}".format(cur_token.value, cur_output), error_type,
                                "Incorrect macro name", mode)
            elif error_type == ErrorType.CommonVarNameError:
                self.logger.log(file_path, cur_token.line,
                                "fixed common var name {} to {}".format(cur_token.value, cur_output), error_type,
                                "Incorrect common var name", mode)
            else:
                self.logger.log(file_path, cur_token.line,
                                "fixed {} to {}".format(cur_token.value, cur_output), error_type,
                                "Unknown error", mode)

    def run_for_project(self, mode, project_path):
        files = []
        tree = os.walk(project_path)
        for d in tree:
            cur_dir_name = d[0]
            cur_dir_files = d[2]
            for file in cur_dir_files:
                if file.endswith(".cpp") or file.endswith(".h"):
                    files.append(os.path.join(cur_dir_name, file))
        for file in files:
            self.run_for_file(mode, file)

    def run_for_dir(self, mode, project_path):
        files = []
        tree = os.walk(project_path)
        for d in tree:
            cur_dir_name = d[0]
            cur_dir_files = d[2]
            for file in cur_dir_files:
                if file.endswith(".cpp") or file.endswith(".h"):
                    files.append(os.path.join(cur_dir_name, file))
            break
        for file in files:
            self.run_for_file(mode, file)

    def run_for_file(self, mode, file_path):
        if mode in ("--verify", "-v"):
            self.fix_code_style(file_path, WorkingMode.VerifyMode)
        elif mode in ("--fix", "-f"):
            self.fix_code_style(file_path, WorkingMode.FixMode)
        else:
            print("Incorrect mode")

    @staticmethod
    def get_prev_token(tokens, index):
        if len(tokens) == 0:
            return None
        while index - 1 >= 0:
            if tokens[index - 1].token_name not in (TokenName.WHITESPACE, TokenName.NEW_LINE):
                return tokens[index - 1]
            else:
                index -= 1
        return None

    @staticmethod
    def show_help():
        with open("Readme.md", 'r', encoding="utf-8") as file:
            print(file.read())

    @staticmethod
    def save_text_in_file(file_path, text):
        with open(file_path, 'w') as file:
            file.write(text)
