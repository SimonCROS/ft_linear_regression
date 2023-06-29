import pyqtgraph as pg
from PySide6.QtWidgets import QMainWindow

def estimate_price(x: float, theta0: float, theta1: float) -> float:
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
