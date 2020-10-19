from Formatter.formatter import *
import sys

if __name__ == '__main__':
    print('C++ code formatter')
    print('####################################\n')
    formatter = Formatter()
    if sys.argv[1] in ("-h", "--help"):
        formatter.show_help()
    elif sys.argv[1] == "--format":
        formatter.configure_formatter(sys.argv[2])
        if sys.argv[3] == "-p":
            formatter.format_files_in_project(sys.argv[4])
        if sys.argv[3] == "-d":
            formatter.format_files_in_dir(sys.argv[4])
        if sys.argv[3] == "-f":
            formatter.format_single_file(sys.argv[4])
    elif sys.argv[1] == "-p":
        formatter.format_files_in_project(sys.argv[2])
    elif sys.argv[1] == "-d":
        formatter.format_files_in_dir(sys.argv[2])
    elif sys.argv[1] == "-f":
        formatter.format_single_file(sys.argv[2])
    elif sys.argv[1] in ("--verify", "-v"):
        formatter.verify_file(sys.argv[2])
    print('\n####################################')
    print('Finished')


