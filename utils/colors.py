class Colors:
    @staticmethod
    def print_yellow(text):
        print("\033[93m" + text + "\033[0m")  # ANSI escape code for yellow

    @staticmethod
    def print_red(text):
        print("\033[91m" + text + "\033[0m")  # ANSI escape code for red