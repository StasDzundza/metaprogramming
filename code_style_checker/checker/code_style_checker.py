import os
from utils.logger import *


class CodeStyleChecker:
    def __init__(self):
        self.logger = Logger("code_style_fixing.log", "code_style_verification.log")

    def check_code_style(self, file_path):
        pass

    def fix_code_style(self, file_path):
        pass

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
        with open("Readme.md") as file:
            print(file.read())

