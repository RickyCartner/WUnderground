"""
Charts are still in testing phase
"""

import sys

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QBarCategoryAxis
from PyQt5.QtCore import QPointF


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(200, 200, 600, 400)
        self.setWindowTitle("Creating Line Chart")


        series = QLineSeries()

        series.append(0, 6)
        series.append(3, 5)
        series.append(3, 8)
        series.append(7, 3)
        series.append(12, 7)

        series << QPointF(11, 1) << QPointF(13, 3) << QPointF(17, 6) << QPointF(18, 3) << QPointF(20, 20)
        chart = QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("Line Chart Example")

        categories = ["Jan", "Feb", "Mar", "Apr", "May"]

        axis = QBarCategoryAxis()
        axis.append(categories)
        chart.createDefaultAxes()
        chart.setAxisX(axis, series)

        chart_view = QChartView(chart)

        vbox = QVBoxLayout()
        vbox.addWidget(chart_view)
        self.setLayout(vbox)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
