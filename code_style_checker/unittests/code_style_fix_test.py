import unittest
import os
from checker.code_style_checker import *
from lexer import *


class TestCodeStyleFix(unittest.TestCase):
    def test_code_style_fix_for_single_file(self):
        code_style_checker = CodeStyleChecker()
        code_style_checker.run_for_file("-f", "TestData/MyClass.cpp")
        self.assertTrue(os.path.exists("TestData/my_class.cpp"))
        lexer1 = Lexer()
        with open("TestData/MyClass.cpp", 'r', encoding='utf-8') as file:
            cpp_code1 = file.read()
        tokens1 = lexer1.tokenize(cpp_code1)

        lexer2 = Lexer()
        with open("TestData/my_class.cpp", 'r', encoding='utf-8') as file:
            cpp_code2 = file.read()
        tokens2 = lexer2.tokenize(cpp_code2)

        self.assertEqual(len(tokens1), len(tokens2))

        with open("TestData/my_class_expected.txt", 'r', encoding='utf-8') as file:
            expected_code = file.read()
        self.assertEqual(expected_code, cpp_code2)