def find_and_replace(file,search,replace):
    with open(file,"r") as r:
        lines = r.read()
    lines = lines.replace(search,replace)
    with open(file,"w") as w:
        w.write(lines)

if __name__ == "__main__":
    find_and_replace("test.txt", "Agatha", "Carly")