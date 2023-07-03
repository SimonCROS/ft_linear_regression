import sys

from utils import estimate, read_output_file

if __name__ == "__main__":
    window = False

    (theta0, theta1) = read_output_file(sys.argv[1] if len(sys.argv) >= 2 else 'output.txt')

    for line in sys.stdin:
        try:
            print(estimate(float(line.strip()), theta0, theta1))
        except ValueError as ex:
            print(str(ex))
