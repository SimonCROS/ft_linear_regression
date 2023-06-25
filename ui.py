import pyqtgraph as pg
from PySide6.QtWidgets import QMainWindow

class GraphWindow(QMainWindow):

    def __init__(self, x_title: str, x: list[float], y_title: str, y: list[float]):
        super(GraphWindow, self).__init__()

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        hour = [1,2,3,4,5,6,7,8,9,10]
        temperature = [30,32,34,32,33,31,29,32,35,45]

        self.graphWidget.setBackground('w')

        self.graphWidget.plot(x, y, pen=None, symbol='o')

        self.graphWidget.setLabel('bottom', x_title)
        self.graphWidget.setLabel('left', y_title)

    def draw_line(self, p1: tuple[float, float], p2: tuple[float, float]):
        pen = pg.mkPen(color=(255, 0, 0), width=2)
        self.graphWidget.plot([p1[0], p2[0]], [p1[1], p2[1]], pen=pen)
