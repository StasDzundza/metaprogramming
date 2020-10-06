from Lexer.patterns import *
from Lexer.Automaton.automaton import *
from Lexer.Automaton.finite_state_machine import *
import re


class Lexer:
    def __init__(self):
        self.tokens = []

    def tokenize(self, file_path):
        self.tokens.clear()
        with open(file_path, 'r') as file:
            line = file.readline()
            while line:
                cur_line = line
                i = 0
                while i < len(cur_line):
                    is_matched = False
                    for pattern_pair in PATTERNS:
                        if isinstance(pattern_pair[0], FiniteStateMachine):
                            automaton = Automaton(pattern_pair[0])
                            match_pos = automaton.match(cur_line, i)
                            if match_pos[0] is not None and match_pos[1] is not None:
                                matched_text = cur_line[match_pos[0]:match_pos[1]]
                                i = match_pos[1]
                                is_matched = True
                                if pattern_pair[1] == TokenName.IDENTIFIER:
                                    if matched_text in KEYWORDS:
                                        self.tokens.append(Token(TokenName.KEYWORD, matched_text))
                                    elif matched_text in DATA_TYPES:
                                        self.tokens.append(Token(TokenName.DATA_TYPE, matched_text))
                                    elif matched_text in ACCESS_MODIFIERS:
                                        self.tokens.append(Token(TokenName.ACCESS_MODIFIER, matched_text))
                                    else:
                                        self.tokens.append(Token(TokenName.IDENTIFIER, matched_text))
                                else:
                                    self.tokens.append(Token(pattern_pair[1], matched_text))
                                break
                        elif isinstance(pattern_pair[0], str):
                            pattern = re.compile(pattern_pair[0])
                            match_pos = pattern.search(cur_line, i)
                            if match_pos is not None and match_pos.start() == i:
                                matched_text = cur_line[match_pos.start():match_pos.end()]
                                is_matched = True
                                i = match_pos.end()
                                self.tokens.append(Token(pattern_pair[1], matched_text))
                    if not is_matched:
                        self.tokens.append(Token(TokenName.ERROR_TOKEN, cur_line[i]))
                        i += 1
                line = file.readline()

        return self.tokens
