__author__ = 'craig'

def main():
    with open("sonnets.txt", "rb") as fin:
        with open("sonnets-processed.txt", "wb") as fout:
            for line in fin:
                line = line.lstrip().rstrip()
                if line == "" or line.isdigit():
                    continue
                else:
                    fout.write(line + "\n")
    print "Finished."

if __name__ == "__main__":
    main()
