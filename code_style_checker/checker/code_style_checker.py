import os

from utils.logger import *
from lexer.lexer import *
from checker.name_formatter import *


class CodeStyleChecker:
    def __init__(self):
        self.logger = Logger("code_style_fixing.log", "code_style_verification.log")

    def check_code_style(self, file_path):
        pass

    def fix_code_style(self, file_path):
        lexer = Lexer()
        with open(file_path, 'r', encoding="utf-8") as file:
            cpp_code = file.read()
        tokens = lexer.tokenize(cpp_code)
        token_stack = []
        output = ""
        i = 0
        while i < len(tokens):
            output = output + tokens[i].value
            i += 1
        formatted_file_name = format_file_name(os.path.basename(file_path))
        dir_name = os.path.dirname(file_path)
        self.save_text_in_file(os.path.join(dir_name, formatted_file_name), output)

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
            self.check_code_style(file_path)
        elif mode in ("--fix", "-f"):
            self.fix_code_style(file_path)
        else:
            print("Incorrect mode")

    @staticmethod
    def show_help():
        with open("Readme.md", 'r', encoding="utf-8") as file:
            print(file.read())

    @staticmethod
    def save_text_in_file(file_path, text):
        with open(file_path, 'w') as file:
            file.write(text)
