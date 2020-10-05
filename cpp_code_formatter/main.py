from Lexer.lexer import *

if __name__ == '__main__':
    print('C++ code formatter')
    print('####################################\n')
    lexer = Lexer()
    lexer.tokenize("Test/test_code.cpp")
