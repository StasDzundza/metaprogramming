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

