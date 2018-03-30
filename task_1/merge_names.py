import sorter
import argparse

def main():
    parser = argparse.ArgumentParser(description="""Merge 2 files.
                                                    Each line in both files should be in format:
                                                    <text> <ID>
                                                    Output file will be in format:
                                                    <text_1> <text_2> <ID>
                                                    Where "text_1" is text entry from the first file and
                                                    "text_2" is text entry from the second file and "ID"
                                                    is the corresponding ID entry.
                                                    In case either file does not have a text entry corresponding
                                                    to an ID from the other file FILLER will be used
                                                    in the output file.""")
    parser.add_argument("first_file_name")
    parser.add_argument("second_file_name")
    parser.add_argument("output_file")
    parser.add_argument("--filler", default="?")
    args = parser.parse_args()

    def get_id(s):
        try:
            return int(s)
        except ValueError:
            return None

    def sort_key(x):
        s = x.split()
        if(len(x) >= 2):
            i = get_id(s[1])
            if(i):
                return i
        return 0

    first = sorter.sort_file(args.first_file_name, sort_key=sort_key, as_temporary=True)
    second = sorter.sort_file(args.second_file_name, sort_key=sort_key, as_temporary=True)
        
    def get_line(f):
        line = f.readline().split()
        while line:
            if(len(line) >= 2):
                line_id = get_id(line[1])
                if(line_id):
                    return (line[0], line_id)
            line = f.readline().split()
        return ()

    with open(args.output_file, "w") as f:
        line_first = get_line(first)
        line_second = get_line(second)

        while line_first and line_second:
            if(line_first[1] == line_second[1]):
                f.write(line_first[0] + " " + line_second[0] + " " + str(line_first[1]) + "\n")
                line_first = get_line(first)
                line_second = get_line(second)
            elif(line_first[1] < line_second[1]):
                f.write(line_first[0] + " " + args.filler + " " + str(line_first[1]) + "\n")
                line_first = get_line(first)
            else:
                f.write(args.filler + " " + line_second[0] + " " + str(line_second[1]) + "\n")
                line_second = get_line(second)

        while line_first:
            f.write(line_first[0] + " " + args.filler + " " + str(line_first[1]) + "\n")
            line_first = get_line(first)

        while line_second:
            f.write(args.filler + " " + line_second[0] + " " + str(line_second[1]) + "\n")
            line_second = get_line(second)

    first.close()
    second.close()

if __name__ == '__main__':
    main()