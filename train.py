import sys
import math

import csv
from PySide6.QtWidgets import QApplication

from utils import GraphWindow, is_float, estimate_price

theta0: float = 0
theta1: float = 0

x_vals_name: str
y_vals_name: str
x_vals: list[float] = []
y_vals: list[float] = []

learning_rate = 0.1

def read_file(file: str):
    global x_vals, x_vals_name, y_vals, y_vals_name
    try:
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0

            for row in csv_reader:
                if len(row) != 2:
                    print(f"Wrong line {line_count} ({row})", file=sys.stderr)
                    exit(1)
                if line_count == 0:
                    x_vals_name = row[0]
                    y_vals_name = row[1]
                    line_count += 1
                else:
                    if not is_float(row[0]):
                        print(f"Wrong line {line_count} ({row[0]}) is not a valid float", file=sys.stderr)
                        exit(1)
                    if not is_float(row[1]):
                        print(f"Wrong line {line_count} ({row[1]}) is not a valid float", file=sys.stderr)
                        exit(1)
                    x_vals.append(float(row[0]))
                    y_vals.append(float(row[1]))
                    line_count += 1
    except Exception as ex:
        print(ex.strerror, file=sys.stderr)
        exit(1)

    if len(x_vals) == 0 or len(y_vals) == 0:
        print(f'Not enough data avaliable.')
        exit(0)

    if len(x_vals) != len(y_vals):
        print(f'Bad file.')
        exit(1)

    print(f'Processed {line_count} lines.')

if __name__ == "__main__":
    window = False
    if "-w" in sys.argv:
        sys.argv.remove("-w")
        window = True

    read_file(sys.argv[1] if len(sys.argv) >= 2 else 'data.csv')

    samples_count = len(x_vals)

    (x_min, x_max, y_min, y_max) = (min(x_vals), max(x_vals), min(y_vals), max(y_vals))
    (x_vals_diff, y_vals_diff) = (x_max - x_min, y_max - y_min)
    
    # Normalise using min-max method
    normalized_x_vals = [(((x - x_min) / x_vals_diff) if x_vals_diff != 0 else 0) for x in x_vals]
    normalized_y_vals = [(((y - y_min) / y_vals_diff) if y_vals_diff != 0 else 0) for y in y_vals]

    old_theta1 = float('inf')
    while not math.isclose(old_theta1, theta1):
        old_theta1 = theta1
        tmp0 = 0
        tmp1 = 0

        for (x, y) in zip(normalized_x_vals, normalized_y_vals):
            estimated = estimate_price(x, theta0, theta1)
            diff = estimated - y
            tmp0 += diff
            tmp1 += diff * x

        theta0 -= learning_rate * (1 / samples_count) * tmp0
        theta1 -= learning_rate * (1 / samples_count) * tmp1

    # Reverse normalization of theta0 and theta1
    theta1 = (theta1 * y_vals_diff / x_vals_diff) if x_vals_diff != 0 else 0
    theta0 = theta0 * y_vals_diff + y_min - theta1 * x_min

    try:
        with open("output.csv", "w") as outfile:
            outfile.write(f'{theta0},{theta1}')
    except Exception as ex:
        print(ex.strerror, file=sys.stderr)
        exit(1)

    if window:
        app = QApplication(sys.argv)
        w = GraphWindow(x_vals_name, x_vals, y_vals_name, y_vals)
        w.drawLine([x_min, estimate_price(x_min, theta0, theta1)], [x_max, estimate_price(x_max, theta0, theta1)])
        w.show()
        app.exec()
