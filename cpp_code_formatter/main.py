from Formatter.formatter import *


if __name__ == '__main__':
    print('C++ code formatter')
    print('####################################\n')
    formatter = Formatter()
    print(formatter.format_file("Test/test_code.cpp"))
    print('\n####################################')
    print('Finished')


