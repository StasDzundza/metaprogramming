from checker.code_style_checker import *


def run_style_checker(command_line_args):
    code_style_checker = CodeStyleChecker()
    if command_line_args[1] in ("-h", "--help"):
        CodeStyleChecker.show_help()
    elif command_line_args[1] in ("--fix", "-f"):
        if command_line_args[2] == "-p":
            print("fix code style in project: {}".format(command_line_args[3]))
            code_style_checker.run_for_project("-p", command_line_args[3])
        elif command_line_args[2] == "-d":
            print("fix code style in directory: {}".format(command_line_args[3]))
            code_style_checker.run_for_dir("-d", command_line_args[3])
        elif command_line_args[2] == "-f":
            print("fix code style in file: {}".format(command_line_args[3]))
            code_style_checker.run_for_file("-f", command_line_args[3])
        else:
            print("Incorrect command line arguments")
    elif command_line_args[1] in ("--verify", "-v"):
        if command_line_args[2] == "-p":
            print("verify code style in project: {}".format(command_line_args[3]))
            code_style_checker.run_for_project("-p", command_line_args[3])
        elif command_line_args[2] == "-d":
            print("verify code style in directory: {}".format(command_line_args[3]))
            code_style_checker.run_for_dir("-d", command_line_args[3])
        elif command_line_args[2] == "-f":
            print("verify code style in file: {}".format(command_line_args[3]))
            code_style_checker.run_for_file("-f", command_line_args[3])
        else:
            print("Incorrect command line arguments")
