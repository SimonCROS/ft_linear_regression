import sys
import math

import csv
from PySide6.QtWidgets import QApplication

from ui import GraphWindow

theta0: float = 0
theta1: float = 0

inputs_name: str
targets_name: str
input: list[float] = []
targets: list[float] = []

learning_rate = 0.1
iterations_count = 1000

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def estimate_price(value: float) -> float:
    global theta0
    global theta1
    return theta0 + (theta1 * value)

if __name__ == "__main__":
    try:
        with open('data.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0

            for row in csv_reader:
                if len(row) != 2:
                    print(f"Wrong line {line_count} ({row})", file=sys.stderr)
                    exit(1)
                if line_count == 0:
                    inputs_name = row[0]
                    targets_name = row[1]
                    line_count += 1
                else:
                    if not is_float(row[0]):
                        print(f"Wrong line {line_count} ({row[0]}) is not a valid float", file=sys.stderr)
                        exit(1)
                    if not is_float(row[1]):
                        print(f"Wrong line {line_count} ({row[1]}) is not a valid float", file=sys.stderr)
                        exit(1)
                    input.append(float(row[0]))
                    targets.append(float(row[1]))
                    line_count += 1
    except Exception as ex:
        print(ex.strerror, file=sys.stderr)
        exit(1)

    print(f'Processed {line_count} lines.')

    samples_count = len(input)
    
    # Normalise using min-max method
    normalized_input = [(x - min(input)) / (max(input) - min(input)) for x in input]
    normalized_targets = [(y - min(targets)) / (max(targets) - min(targets)) for y in targets]

    for i in range(iterations_count):
        tmp0 = 0
        tmp1 = 0

        for (value, observed) in zip(normalized_input, normalized_targets):
            # print(value, estimate_price(value), observed)
            estimated = estimate_price(value)
            diff = estimated - observed

            tmp0 += diff
            tmp1 += diff * value

        theta0 -= learning_rate * (1 / samples_count) * tmp0
        theta1 -= learning_rate * (1 / samples_count) * tmp1

    input_diff = max(input) - min(input)
    targets_diff = max(targets) - min(targets)

    theta1 = theta1 * targets_diff / input_diff
    theta0 = theta0 * targets_diff + min(targets) - theta1 * min(input)

    print(f"theta0 = {theta0}, theta1 = {theta1}")
    print(estimate_price(0))

    app = QApplication(sys.argv)
    w = GraphWindow(inputs_name, input, targets_name, targets)
    w.drawLine([min(input), estimate_price(min(input))], [max(input), estimate_price(max(input))])
    w.show()
    app.exec()
