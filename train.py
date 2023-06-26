import sys
import math

import csv
from PySide6.QtWidgets import QApplication

from ui import GraphWindow

theta0: float = 0
theta1: float = 0

mean: float = 0
std: float = 0

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

def estimate_price(mileage: float) -> float:
    global theta0
    global theta1
    return theta0 + (theta1 * mileage)

def normalize(value):
    global mean
    global std
    return (value - mean) / std

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
    
    mean = sum(input) / len(input)
    variance = sum(pow(x - mean, 2) for x in input) / len(input)
    std = math.sqrt(variance)
    
    # Normalise will set the mean to 0 and the standard deviation at 1
    normalized_input = list(map(normalize, input))

    for i in range(iterations_count):
        tmp0 = 0
        tmp1 = 0

        for (value, observed) in zip(normalized_input, targets):
            # print(value, estimate_price(value), observed)
            estimated = estimate_price(value)
            diff = estimated - observed

            tmp0 += diff
            tmp1 += diff * value

        theta0 -= learning_rate * (1 / samples_count) * tmp0
        theta1 -= learning_rate * (1 / samples_count) * tmp1

    print(f"theta0 = {theta0}, theta1 = {theta1}")

    app = QApplication(sys.argv)
    w = GraphWindow(inputs_name, input, targets_name, targets)
    w.drawLine([min(input), estimate_price(normalize(min(input)))], [max(input), estimate_price(normalize(max(input)))])
    w.show()
    app.exec()
