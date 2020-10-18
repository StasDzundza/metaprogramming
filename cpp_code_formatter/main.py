from Formatter.formatter import *
import sys

if __name__ == '__main__':
    print('C++ code formatter')
    print('####################################\n')
    # with open("Test/test_code.cpp", 'r', encoding="utf-8") as file:
    #     text = file.read()
    # lexer = Lexer()
    # tokens = lexer.tokenize(text)
    # for token in tokens:
    #     print(token.to_string())
    formatter = Formatter()
    if sys.argv[1] in ("-h", "--help"):
        formatter.show_help()
    elif sys.argv[1] in ("--format", "-f"):
        # set path to config in formatter
        formatter.set_config_path(sys.argv[2])
        if sys.argv[3] == "-p":
            formatter.format_files_in_project(sys.argv[4])
        if sys.argv[3] == "-d":
            formatter.format_files_in_dir(sys.argv[4])
        if sys.argv[3] == "-f":
            formatter.format_file(sys.argv[4])
    elif sys.argv[1] == "-p":
        formatter.format_files_in_project(sys.argv[2])
    elif sys.argv[1] == "-d":
        formatter.format_files_in_dir(sys.argv[2])
    elif sys.argv[1] == "-f":
        formatter.format_file(sys.argv[2])
    elif sys.argv[1] in ("--verify", "-v"):
        formatter.verify_file(sys.argv[2])
    print('\n####################################')
    print('Finished')


