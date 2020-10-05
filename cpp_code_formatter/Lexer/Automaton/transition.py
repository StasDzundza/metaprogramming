class Transition:
    def is_possible(self, c):
        pass


class SymbolTransition(Transition):
    def __init__(self, symbol, state):
        self.symbol = symbol
        self.state = state

    def is_possible(self, c):
        return c == self.symbol


class FuncTransition(Transition):
    def __init__(self, transition_function, state):
        self.transition_function = transition_function
        self.state = state

    def is_possible(self, c):
        return self.transition_function(c)
