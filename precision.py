import sys
import math

from utils import read_csv_file, read_output_file, estimate

if __name__ == "__main__":
    window = False
    if "-w" in sys.argv:
        sys.argv.remove("-w")
        window = True

    (_, x_vals, _, y_vals) = read_csv_file(sys.argv[1] if len(sys.argv) >= 2 else 'data.csv')
    (theta0, theta1) = read_output_file(sys.argv[2] if len(sys.argv) >= 3 else 'output.txt')

    samples_count = len(x_vals)

    mae = 0
    mse = 0
    mape = 0
    for (x, y) in zip(x_vals, y_vals):
        estimated = estimate(x, theta0, theta1)
        mae += abs(estimated - y)
        mse += pow(estimated - y, 2)
        if y != 0:
            mape += abs((y - estimated) / y) * 100

    mae /= samples_count
    mse /= samples_count
    mape /= samples_count - y_vals.count(0)

    print(" MAE: {:.2f}".format(mae))
    print(" MSE: {:.2f}".format(mse))
    print("RMSE: {:.2f}".format(math.sqrt(mse)))
    print("MAPE: {:.2f}%".format(mape))
