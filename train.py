import csv
import sys

theta0: float = 0
theta1: float = 0

mileages: list[float] = []
prices: list[float] = []

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def estimate_price(mileage: float) -> float:
    global theta0
    global theta1
    return theta0 + (theta1 * mileage)

if __name__ == "__main__":
    with open('data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                if len(row) != 2:
                    print(f"Wrong line {line_count} ({row})", file=sys.stderr)
                    exit(1)
                if not is_float(row[0]):
                    print(f"Wrong line {line_count} ({row[0]}) is not a valid float", file=sys.stderr)
                    exit(1)
                if not is_float(row[1]):
                    print(f"Wrong line {line_count} ({row[1]}) is not a valid float", file=sys.stderr)
                    exit(1)
                mileages.append(float(row[0]))
                prices.append(float(row[1]))
                line_count += 1
        print(f'Processed {line_count} lines.')
        tmp0 = 1 * (1 / len(prices))
