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

    n_failed = 0
    for idx, test in enumerate(TESTS):
        output = check_bracket_balance(test[0])
        if(test[1] != output):
            n_failed += 1
            print("Failed test %d.\nInput: %s\nExpected output: %s\nOutput: %s" % (idx, test[0], test[1], output))
    print("Failed tests: %d / %d" % (n_failed, len(TESTS)))

if __name__ == '__main__':
    main()