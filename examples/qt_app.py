"""
Qt app
------

An example demonstrating a qt app with a wgpu viz inside.

Note how the ``rendercanvas.qt.loop`` object is not even imported;
you can simply run ``app.exec()`` the Qt way.
"""

# ruff: noqa: N802, E402

import time
import importlib


# Normally you'd just write e.g.
# from PySide6 import QtWidgets

# For the sake of making this example Just Work, we try multiple QT libs
for lib in ("PySide6", "PyQt6", "PySide2", "PyQt5"):
    try:
        QtWidgets = importlib.import_module(".QtWidgets", lib)
        break
    except ModuleNotFoundError:
        pass

from rendercanvas.qt import QRenderWidget
from rendercanvas.utils.cube import setup_drawing_sync


class ExampleWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1260, 480)
        self.setWindowTitle("Rendering to a canvas embedded in a qt app")

        splitter = QtWidgets.QSplitter()

        self.button = QtWidgets.QPushButton("Hello world", self)
        self.canvas_bitmap = QRenderWidget(splitter, update_mode="continuous", present_method="bitmap", title="bitmap widget")
        self.canvas_screen = QRenderWidget(splitter, update_mode="continuous", present_method="screen", title="screen widget")
        self.output = QtWidgets.QTextEdit(splitter)

        self.button.clicked.connect(self.whenButtonClicked)
        self.canvas_bitmap.add_event_handler(self.whenCanvasClicked, "pointer_down")
        self.canvas_screen.add_event_handler(self.whenCanvasClicked, "pointer_down")

        # TODO: have some labels to indicate which canvas is which? (does this need to wrap the canvas inside some container widget?)
        splitter.addWidget(self.canvas_bitmap)
        splitter.addWidget(self.canvas_screen)
        splitter.addWidget(self.output)
        splitter.setSizes([400, 400, 200])

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.button, 0)
        layout.addWidget(splitter, 1)
        self.setLayout(layout)

        self.show()

    def addLine(self, line):
        t = self.output.toPlainText()
        t += "\n" + line
        self.output.setPlainText(t)

    def whenButtonClicked(self):
        self.addLine(f"Clicked at {time.time():0.1f}")

    def whenCanvasClicked(self, event):
        # TODO: can we figure out which canvas was clicked? (to show it's present_method perhaps)...
        self.addLine(f"Canvas clicked at {time.time():0.1f}, {event=}")


app = QtWidgets.QApplication([])
example = ExampleWidget()


draw_frame_bitmap = setup_drawing_sync(example.canvas_bitmap)
example.canvas_bitmap.request_draw(draw_frame_bitmap)

draw_frame_screen = setup_drawing_sync(example.canvas_screen)
example.canvas_screen.request_draw(draw_frame_screen)

# Enter Qt event-loop (compatible with qt5/qt6)
app.exec() if hasattr(app, "exec") else app.exec_()
