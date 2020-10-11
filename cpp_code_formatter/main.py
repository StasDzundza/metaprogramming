from Formatter.formatter import *


if __name__ == '__main__':
    print('C++ code formatter')
    print('####################################\n')
    formatter = Formatter()
    formatter.format_files_in_dir("Test")
    print('\n####################################')
    print('Finished')


