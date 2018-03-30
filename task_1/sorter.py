import tempfile
import queue

def sort_file(file_name, sort_key=lambda x: x, as_temporary=False, sorted_file_name=None, lines_per_chunk=100000):
    if(lines_per_chunk < 1):
        raise ValueError("lines_per_chunk argument should be an integer greater than 0")

    if(sorted_file_name is None):
        sorted_file_name = "sorted_" + file_name

    def add_new_chunk(lines):
        lines = sorted(lines, key=sort_key)
        tmpfile = tempfile.TemporaryFile(mode="w+")
        tmpfile.write("".join(lines[1:]))
        tmpfile.seek(0)
        chunks.put((sort_key(lines[0]), lines[0], tmpfile))

    chunks = queue.PriorityQueue()
    with open(file_name, "r") as f:
        lines = []
        for line in f:
            lines.append(line)

            if(len(lines) >= lines_per_chunk):
                add_new_chunk(lines)
                lines = []
        if(lines):
            add_new_chunk(lines)

    if(as_temporary):
        f = tempfile.TemporaryFile(mode="w+")
    else:
        f = open(sorted_file_name, "w+")

    while not chunks.empty():
        _, line, tmpfile = chunks.get()
        f.write(line)

        next_line = tmpfile.readline()
        if(next_line):
            chunks.put((sort_key(next_line), next_line, tmpfile))
        else:
            tmpfile.close()

    f.seek(0)
    return f