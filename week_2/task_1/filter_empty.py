import sys

def main():
    for line in sys.stdin:
        if line.isspace():
            continue
        sys.stdout.write(line)

main()
