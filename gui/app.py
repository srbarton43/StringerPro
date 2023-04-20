from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QHBoxLayout, 
    QLabel, 
    QLineEdit, 
    QVBoxLayout, 
    QWidget, 
    QComboBox,
    QListWidget
)
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stringing Info") 
        self.setFixedSize(QSize(400,300))

        self.dropdown = QComboBox()
        self.dropdown.addItems(["Babolat","Head","Wilson","Yonex"])
        self.dropdown.currentIndexChanged.connect(self.brandChanged)

        self.label = QLabel("Select Brand:")
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.input = QLineEdit()
        self.input.returnPressed.connect(self.returnPressed)

        self.models = QListWidget()
        self.models.addItems(["1","2","3","4"])
        self.models.itemClicked.connect(self.modelClicked)

        layout = QVBoxLayout()
        brandLayout = QHBoxLayout()
        brandLayout.addWidget(self.label)
        brandLayout.addWidget(self.dropdown)
        layout.addLayout(brandLayout)
        layout.addWidget(self.input)
        layout.addWidget(self.models)

        layout.setContentsMargins(10,5,10,10)
        layout.setSpacing(5)
        container = QWidget()
        container.setLayout(layout)

        # Set the central widget of the Window.
        self.setCentralWidget(container)
    # drop down picking brand handling
    def brandChanged(self, i):
        print(i)
    # handling search query
    def returnPressed(self):
        print(self.input.text())
        self.input.setText("")

    # for selecting model to show specs for
    def modelClicked(self,item):
        print("clicked",item.text())

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
window = MainWindow()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()


# Your application won't reach here until you exit and the event
# loop has stopped.