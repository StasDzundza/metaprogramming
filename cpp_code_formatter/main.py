from Lexer.lexer import *

if __name__ == '__main__':
    print('C++ code formatter')
    print('####################################\n')
    lexer = Lexer()
    tokens = lexer.tokenize("Test/test_code.cpp")
    for token in tokens:
        print(token.to_string())
