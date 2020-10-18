########################## WHITESPACE CONFIG FLAGS ##################################
# indents
indent_len = 4

#  before parentheses
func_decl_parenthesis = False  # TODO implement
if_parenthesis = True
for_parenthesis = True
while_parenthesis = True
switch_parenthesis = True
catch_parenthesis = True

# around operators
around_assignment_op = True
around_logical_op = True
around_equality_op = True
around_relational_op = True  # TODO implement <=> token parsing
around_bitwise_op = True
around_additive_op = True
around_multiplicative_op = True
around_shift_op = True
around_unary_op = True  # !, -, +, ++, --  TODO implement
around_pointer_to_member_op = False

# before left brace
before_ns_left_brace = False
before_init_list_left_brace = False
before_class_struct_left_brace = True
before_function_left_brace = True  # TODO implement
before_if_left_brace = True
before_else_left_brace = True
before_for_left_brace = True
before_while_left_brace = True
before_do_left_brace = True
before_switch_left_brace = True
before_try_left_brace = True
before_catch_left_brace = True

# before keywords
before_else = True
before_while = True
before_catch = True

# in ternary operator
before_ternary = True
before_colon_ternary = True
after_colon_ternary = True
after_ternary = True