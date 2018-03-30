import argparse
import random
import string

def get_random_ascii_string(size=20):
    return "".join(random.choices(string.ascii_lowercase, k=size))

def main():
    parser = argparse.ArgumentParser(description="""Generates 2 files.\n
                                                    Format of each line of the first file:\n
                                                    <lower_case_letters> <number>\n
                                                    Format of each line of the second file:\n
                                                    <upper_case_letters> <number>\n
                                                    Letters next to the same numbers in the files will be the same
                                                    (just with different cases)""")
    parser.add_argument("first_file_name")
    parser.add_argument("second_file_name")
    parser.add_argument("-n", "--n-lines", default=1000, type=int)
    args = parser.parse_args()

    with open(args.first_file_name, 'w') as f1, open(args.second_file_name, 'w') as f2:
        LINES_PER_ROUND = 500000

        lines_remaining = args.n_lines
        current_line = 1
        while lines_remaining > 0:
            lines_generated = min(LINES_PER_ROUND, lines_remaining)

            lines1 = []
            lines2 = []
            for _ in range(lines_generated):
                text = get_random_ascii_string()

                lines1.append(text + " " + str(current_line) + "\n")
                lines2.append(text.upper() + " " + str(current_line) + "\n")

                current_line += 1

            random.shuffle(lines1)
            random.shuffle(lines2)

            f1.write("".join(lines1))
            f2.write("".join(lines2))

            lines_remaining -= lines_generated

if __name__ == '__main__':
    main()