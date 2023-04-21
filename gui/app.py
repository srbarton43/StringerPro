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
    QListWidget,
    QStackedLayout,
    QTableWidget,
    QHeaderView,
    QTableWidgetItem
)
import sys
from pathlib import Path
path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))
print(sys.path)
import scraper as s

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stringing Info") 
        self.setFixedSize(QSize(650,400))

        self.brand = s.Brand("babolat")
        
        self.label = QLabel("Select Brand:")
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight)

        keys = []
        for key in self.brand.allowedBrands.keys():
            keys.append(key.capitalize())
        self.dropdown = QComboBox()
        self.dropdown.addItems(keys)
        self.dropdown.currentTextChanged.connect(self.brandChanged)

        self.input = QLineEdit()
        self.input.returnPressed.connect(self.returnPressed)

        self.models = QListWidget()
        self.models.itemClicked.connect(self.modelClicked)

        self.specs = QTableWidget(1,8)
        self.specs.setHorizontalHeaderLabels(["Model","Tension","Length","Pattern","Skip M Holes","Tie Off M","Start C","Tie Off C"])
        self.specs.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)      
        self.specs.verticalHeader().setVisible(False)
        
        self.models.addItems(self.brand.getListOfModels(""))

        layout = QVBoxLayout()
        brandLayout = QHBoxLayout()
        brandLayout.addWidget(self.label)
        brandLayout.addWidget(self.dropdown)
        layout.addLayout(brandLayout)
        
        layout.addWidget(self.input)

        self.stackLayout = QStackedLayout()
        self.stackLayout.addWidget(self.models)
        self.stackLayout.addWidget(self.specs)
        layout.addLayout(self.stackLayout)

        layout.setContentsMargins(10,5,10,10)
        layout.setSpacing(5)
        container = QWidget()
        container.setLayout(layout)

        # Set the central widget of the Window.
        self.setCentralWidget(container)

    # drop down picking brand handling
    def brandChanged(self, b):
        self.brand = s.Brand(b.lower())
        self.stackLayout.setCurrentIndex(0)
        self.models.clear()
        self.models.addItems(self.brand.getListOfModels(""))
    # handling search query
    def returnPressed(self):
        self.models.clear()
        self.models.addItems(self.brand.getListOfModels(self.input.text()))
        self.stackLayout.setCurrentIndex(0)
        self.input.setText("")

    # for selecting model to show specs for
    def modelClicked(self,item):
        self.stackLayout.setCurrentIndex(1)
        self.specs.setItem(0,0, QTableWidgetItem(item.text()))
        for i in range(1,8):
            self.specs.setItem(0,i,QTableWidgetItem(self.brand.getSpecs(item.text())[i-1]))

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