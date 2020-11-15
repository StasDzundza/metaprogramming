import unittest
import math
from checker.name_formatter import *


class TestNameFormatter(unittest.TestCase):
    def test_common_name_formatting(self):
        self.assertEqual("common_var_name", format_common_var_name("CommonVarName"))
        self.assertEqual("common_var_name", format_common_var_name("commonVarName"))
        self.assertEqual("common_var_name", format_common_var_name("Common_Var_Name"))
        self.assertEqual("common_var_name1", format_common_var_name("Common_Var_Name1"))
        self.assertEqual("common_var_name", format_common_var_name("common_var_name"))
        self.assertEqual("common_var_name", format_common_var_name("Common_var_name"))

    def test_class_member_name_formatting(self):
        self.assertEqual("class_var_name_", format_class_var_name("class_var_name"))
        self.assertEqual("class_var_name_", format_class_var_name("ClassVarName"))
        self.assertEqual("class_var_name_", format_class_var_name("classVarName"))
        self.assertEqual("class_var_name1_", format_class_var_name("classVarName1"))
        self.assertEqual("class_var_name_", format_class_var_name("class_Var_Name"))
        self.assertEqual("class_var_name_", format_class_var_name("Class_Var_name"))
        self.assertEqual("class_var_name_", format_class_var_name("Class_Var_Name"))

    def test_const_and_enum_var_formatting(self):
        self.assertEqual("kConstVar", format_const_var_name("const_var"))
        self.assertEqual("kConstVar", format_const_var_name("Const_Var"))
        self.assertEqual("kConstVar", format_const_var_name("ConstVar"))
        self.assertEqual("kConstVar", format_const_var_name("Const_________________Var"))
        self.assertEqual("kConstVar", format_const_var_name("kConstVar"))
        self.assertEqual("kConstVar8_0_0", format_const_var_name("kConstVar8_0_0"))

    def test_macro_name_formatting(self):
        self.assertEqual("PI_VALUE", format_macro_name("pi_value"))
        self.assertEqual("PI_VALUE", format_macro_name("Pi_Value"))
        self.assertEqual("PI_VALUE", format_macro_name("pi_Value"))
        self.assertEqual("PI_VALUE", format_macro_name("Pi_value"))
        self.assertEqual("PI_VALUE", format_macro_name("piValue"))
        self.assertEqual("PI_VALUE", format_macro_name("PI_VALUE"))

    def test_func_name_formatting(self):
        self.assertEqual("FuncName", format_func_name("func_name"))
        self.assertEqual("FuncName", format_func_name("func_Name"))
        self.assertEqual("FuncName", format_func_name("Func_Name"))
        self.assertEqual("FuncName", format_func_name("Func_name"))
        self.assertEqual("FuncName", format_func_name("___FuncName"))
        self.assertEqual("FuncName", format_func_name("FuncName___"))
        self.assertEqual("FuncName", format_func_name("FuncName"))
        self.assertEqual("FuncName", format_func_name("Func__________________Name"))
        self.assertEqual("FuncName", format_func_name("___func__________________name___"))

    def test_type_name_formatting(self):
        self.assertEqual("TypeName", format_type_name("type_name"))
        self.assertEqual("TypeName", format_type_name("type_Name"))
        self.assertEqual("TypeName", format_type_name("Type_Name"))
        self.assertEqual("TypeName", format_type_name("Type_name"))
        self.assertEqual("TypeName", format_type_name("___TypeName"))
        self.assertEqual("TypeName", format_type_name("___TypeName___"))
        self.assertEqual("TypeName", format_type_name("___Type______Name___"))

    def test_file_name_formatting(self):
        self.assertEqual("some_file_name.cpp", format_file_name("SomeFileName.cpp"))
        self.assertEqual("some_file_name.cpp", format_file_name("Some_File_Name.cpp"))
        self.assertEqual("some_file_name.cpp", format_file_name("some_File_Name.cpp"))
        self.assertEqual("some_file_name.cpp", format_file_name("some_file_Name.cpp"))
        self.assertEqual("some_file_name.cpp", format_file_name("some_file_name.cpp"))
        self.assertEqual("some-file-name.cpp", format_file_name("Some-File-Name.cpp"))
        self.assertEqual("some-file-name.cpp", format_file_name("Some-File-Name.cpp"))

    def test_single_line_comment_formatting(self):
        comment = self.__generate_comment(80, 'a')
        self.assertEqual(1, format_single_line_comment(comment).count('\n'))
        comment = comment + "\n\n\n\n\n\n\n\n"
        self.assertEqual(2, format_single_line_comment(comment).count('\n'))
        comment = self.__generate_comment(1000, 'a')
        self.assertEqual(math.ceil(1000 / 80), format_single_line_comment(comment).count('\n'))
        self.assertEqual("// some single line comment\n", format_single_line_comment("//some     single line     "
                                                                                     "comment"))

    def test_multiline_comment_formatting(self):
        self.assertEqual("// some multi line comment\n", format_multi_line_comment("/*some     multi line     "
                                                                                   "comment*/"))

    @staticmethod
    def __generate_comment(length, symbol):
        comment = '//'
        for i in range(0, length):
            comment = comment + symbol
        return comment
