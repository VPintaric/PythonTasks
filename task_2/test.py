from check_brackets import check_bracket_balance

def main():
    TESTS = [
        ("(((((())))))", True),
        ("[][][][][][][]", True),
        ("[{[{}]]", False),
        ("[[([[[(", False),
        ("[(])", False),
        ("(){}[]()[]{}", True),
        ("P(y)th[on i]s a.n e{a()sy} {[()]}(t[])o learn [lang]u{age}...", True),
        ("[P(y)th[on i]s a.n e{a()sy} {[()]}(t[])o learn [lang]u{age}...]]", False)
    ]

    n_passed = 0
    for idx, test in enumerate(TESTS):
        output = check_bracket_balance(test[0])
        if(test[1] != output):
            print("Test %d FAILED\nInput: %s\nExpected output: %s\nOutput: %s\n" % (idx, test[0], test[1], output))
        else:
            n_passed += 1
            print("Test %d PASSED" % idx)
    print("Passed tests: %d / %d" % (n_passed, len(TESTS)))

if __name__ == '__main__':
    main()