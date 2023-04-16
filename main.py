if __name__ == '__main__':
    f = open("txt/txt2")
    lines = []
    line = f.readline()
    while line:
        l = line.replace('\n', '')
        if len(l) > 0:
            print(l)
            lines.append(l)
        line = f.readline()
    print(lines)