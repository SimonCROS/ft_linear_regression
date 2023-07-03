import sys

import csv
import pyqtgraph as pg
from PySide6.QtWidgets import QMainWindow

def estimate(x: float, theta0: float, theta1: float) -> float:
    return theta0 + (theta1 * x)

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

class GraphWindow(QMainWindow):

    def __init__(self, x_title: str, x: list[float], y_title: str, y: list[float]):
        super(GraphWindow, self).__init__()

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)
        self.graphWidget.setMouseEnabled(False, False)

        self.graphWidget.setBackground('w')

        self.graphWidget.plot(x, y, pen=None, symbol='o')

        self.graphWidget.setLabel('bottom', x_title)
        self.graphWidget.setLabel('left', y_title)

    def drawLine(self, p1: tuple[float, float], p2: tuple[float, float]):
        pen = pg.mkPen(color=(255, 0, 0), width=2)
        self.graphWidget.plot([p1[0], p2[0]], [p1[1], p2[1]], pen=pen)

def read_csv_file(file: str) -> tuple[str, list[float], str, list[float]]:
    x_vals_name = ""
    x_vals = []
    y_vals_name = ""
    y_vals = []
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
        print(f"Cannot read the input file: {str(ex)}", file=sys.stderr)
        exit(1)

    if len(x_vals) == 0 or len(y_vals) == 0:
        print(f'Not enough data avaliable.')
        exit(0)

    if len(x_vals) != len(y_vals):
        print(f'Bad file.')
        exit(1)

    print(f'Processed {line_count} lines.')
    return (x_vals_name, x_vals, y_vals_name, y_vals)
