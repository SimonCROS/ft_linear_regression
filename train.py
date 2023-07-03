import sys
import math

from PySide6.QtWidgets import QApplication

from utils import GraphWindow, read_csv_file, estimate

learning_rate = 0.5

if __name__ == "__main__":
    window = False
    if "-w" in sys.argv:
        sys.argv.remove("-w")
        window = True

    (x_vals_name, x_vals, y_vals_name, y_vals) = read_csv_file(sys.argv[1] if len(sys.argv) >= 2 else 'data.csv')

    samples_count = len(x_vals)

    (x_min, x_max, y_min, y_max) = (min(x_vals), max(x_vals), min(y_vals), max(y_vals))
    (x_vals_diff, y_vals_diff) = (x_max - x_min, y_max - y_min)
    
    # Normalise using min-max method
    normalized_x_vals = [(((x - x_min) / x_vals_diff) if x_vals_diff != 0 else 0) for x in x_vals]
    normalized_y_vals = [(((y - y_min) / y_vals_diff) if y_vals_diff != 0 else 0) for y in y_vals]

    theta0: float = 0
    theta1: float = 0

    i = 0
    old_theta1 = float('inf')
    while not math.isclose(old_theta1, theta1):
        old_theta1 = theta1
        tmp0 = 0
        tmp1 = 0

        for (x, y) in zip(normalized_x_vals, normalized_y_vals):
            estimated = estimate(x, theta0, theta1)
            diff = estimated - y
            tmp0 += diff
            tmp1 += diff * x

        theta0 -= learning_rate * (1 / samples_count) * tmp0
        theta1 -= learning_rate * (1 / samples_count) * tmp1

        i += 1

        if not math.isfinite(theta1):
            print("Learning rate too big, abort", file=sys.stderr)
            exit(1)

    # Reverse normalization of theta0 and theta1
    theta1 = (theta1 * y_vals_diff / x_vals_diff) if x_vals_diff != 0 else 0
    theta0 = theta0 * y_vals_diff + y_min - theta1 * x_min

    print(f"Regression finished after {i} cycles")

    try:
        with open("output.txt", "w") as outfile:
            outfile.write(f'{theta0},{theta1}')
    except Exception as ex:
        print(f"Cannot write the output file: {str(ex)}", file=sys.stderr)
        exit(1)

    if window:
        app = QApplication(sys.argv)
        w = GraphWindow(x_vals_name, x_vals, y_vals_name, y_vals)
        w.drawLine([x_min, estimate(x_min, theta0, theta1)], [x_max, estimate(x_max, theta0, theta1)])
        w.show()
        app.exec()
