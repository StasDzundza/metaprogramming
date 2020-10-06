from Lexer.Automaton.transition import *
from Lexer.Automaton.state import *
from Lexer.Automaton.finite_state_machine import *


def bracket_state_machine():
    initial = State(False)
    q1 = State(True)  # (
    q2 = State(True)  # )
    q3 = State(True)  # {
    q4 = State(True)  # }
    q5 = State(True)  # [
    q6 = State(True)  # ]

    initial.add_transition(SymbolTransition("(", q1))
    initial.add_transition(SymbolTransition(")", q2))
    initial.add_transition(SymbolTransition("{", q3))
    initial.add_transition(SymbolTransition("}", q4))
    initial.add_transition(SymbolTransition("[", q5))
    initial.add_transition(SymbolTransition("]", q6))
    return FiniteStateMachine(initial)


def separator_state_machine():
    initial = State(False)
    q1 = State(True)  # :
    q2 = State(True)  # ,
    q3 = State(True)  # ;

    initial.add_transition(SymbolTransition(":", q1))
    initial.add_transition(SymbolTransition(",", q2))
    initial.add_transition(SymbolTransition(";", q3))
    return FiniteStateMachine(initial)


def whitespace_state_machine():
    initial = State(False)
    q1 = State(True)

    func_transition = lambda c: c == ' ' or c == '\t'
    q1.add_transition(FuncTransition(func_transition, q1))
    initial.add_transition(FuncTransition(func_transition, q1))
    return FiniteStateMachine(initial)


def new_line_state_machine():
    initial = State(False)
    q1 = State(True)
    transition_function = lambda c: c == '\n' or c == '\r'
    initial.add_transition(FuncTransition(transition_function, q1))
    return FiniteStateMachine(initial)


def double_quote_string_state_machine():
    initial = State(False)
    q1 = State(False)
    q2 = State(True)
    q3 = State(False)

    str_symbols = lambda c: c != '\"' and c != '\\'
    not_slash = lambda c: c != '\\'

    q1.add_transition(FuncTransition(str_symbols, q1))
    q1.add_transition(SymbolTransition('\\', q3))
    q3.add_transition(SymbolTransition('\\', q3))
    q3.add_transition(FuncTransition(not_slash, q1))
    q1.add_transition(SymbolTransition('\"', q2))  # end string
    initial.add_transition(SymbolTransition('\"', q1))
    return FiniteStateMachine(initial)


def identifier_state_machine():
    initial = State(False)
    q1 = State(True)
    start_name_transition = lambda c: c == '_' or c.isalpha()
    initial.add_transition(FuncTransition(start_name_transition, q1))
    name_transition = lambda c: c == '_' or c.isalpha() or c.isdigit()
    q1.add_transition(FuncTransition(name_transition, q1))
    return FiniteStateMachine(initial)


def number_state_machine():
    initial = State(False)
    q1 = State(True)
    transition_function = lambda c: c.isdigit()
    initial.add_transition(FuncTransition(transition_function, q1))
    q1.add_transition(FuncTransition(transition_function, q1))
    return FiniteStateMachine(initial)


def char_symbol_state_machine():
    initial = State(False)
    q1 = State(False)  # '
    q2 = State(False)  # symbol
    q3 = State(True)   # '
    initial.add_transition(SymbolTransition('\'', q1))
    q1.add_transition(FuncTransition(lambda c: c.isalpha(), q2))
    q2.add_transition(SymbolTransition('\'', q3))
    return FiniteStateMachine(initial)