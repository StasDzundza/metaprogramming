class Lexer:
    def __init__(self):
        self.tokens = []

    def tokenize(self, file_path):
        self.tokens.clear()
        with open(file_path, 'r') as file:
            line = " "
            while line:
                line = file.readline()
                print(line, end="")
        return self.tokens
