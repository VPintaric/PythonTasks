import argparse
import sys
import logging

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
    logging.basicConfig(format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser(description="""Checks if the braces (\"()\", \"{}\", \"[]\")
                                        in the given input are balanced. Reads input from file if 
                                        file name is given, otherwise reads from standard input.""")
    parser.add_argument("input_file_name", nargs="?")
    args = parser.parse_args()

    if(args.input_file_name is None):
        f = sys.stdin
    else:
        try:
            f = open(args.input_file_name, "r")
        except IOError:
            logging.error("Cannot open \"%s\"" % args.input_file_name)
            return

    text = f.read()
    if(check_bracket_balance(text)):
        print("Brackets are balanced")
    else:    
        print("Brackets are unbalanced")

    f.close()


if __name__ == '__main__':
    main()