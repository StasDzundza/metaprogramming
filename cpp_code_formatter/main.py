import Lexer.lexer
import Formatter.formatter


if __name__ == '__main__':
    print('C++ code formatter')
    print('####################################\n')
    lexer = Lexer()
    tokens = lexer.tokenize("Test/test_code.cpp")
    for token in tokens:
        print(token.to_string())
    print('\n####################################')
    print('Finished')


