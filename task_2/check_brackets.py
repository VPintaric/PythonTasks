import argparse
import sys

UNBALANCED_BRACKETS_MSG = "Brackets are unbalanced"
BALANCED_BRACKETS_MSG = "Brackets are balanced"

def check_bracket_balance(text):
    OPEN_BRACKETS = "([{"
    CLOSE_BRACKETS = ")]}"
    MATCHING_BRACKETS = {")" : "(", 
                        "]" : "[",
                        "}" : "{"}

    stack = []
    for c in text:
        if c in OPEN_BRACKETS:
            stack.append(c)
        elif c in CLOSE_BRACKETS:
            if(not stack or MATCHING_BRACKETS[c] != stack.pop()):
                return False
    return not stack

def main():
    parser = argparse.ArgumentParser(description="""Checks if the braces (\"()\", \"{}\", \"[]\")
                                        in the given input are balanced. Reads input from file if 
                                        file name is given, otherwise reads from standard input.""")
    parser.add_argument("input_file_name", nargs="?")
    args = parser.parse_args()

    if(args.input_file_name is None):
        f = sys.stdin
    else:
        f = open(args.input_file_name, "r")
    text = f.read()

    if(check_bracket_balance(text)):
        print(BALANCED_BRACKETS_MSG)
    else:    
        print(UNBALANCED_BRACKETS_MSG)

    f.close()


if __name__ == '__main__':
    main()