#!/usr/bin/env python
"""
GUI App for Running Scraper and Letting User Interact with Results
Pretty intuitive app design...pick a rackquet brand, and then either search \
    for a model or scroll and select it from field
Upon selection, all important racquet specifications will be displayed

Sam Barton 2023
"""
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
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
import tennis_scraper.scraper as s

PLACEHOLDER = "Set Input Text"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stringing Info")
        self.setFixedSize(QSize(650, 400))

        # all of the scraping upon open
        self.dir = s.Directory()
        self.brand = self.dir.brands[0]

        self.label = QLabel("Select Brand:")
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.label.setStyleSheet("padding-top: 10px;"
                                 "padding-left: 40px;"
                                 "padding-right: 0px;"
                                 "padding-bottom: 12px;")

        keys = []
        for key in self.dir.brandsMap.keys():
            keys.append(key)
        self.dropdown = QComboBox()
        self.dropdown.addItems(keys)
        self.dropdown.currentIndexChanged.connect(self.brandChanged)

        self.input = QLineEdit()
        self.input.returnPressed.connect(self.returnPressed)
        self.input.setPlaceholderText(PLACEHOLDER)

        self.searchButton = QPushButton("Search")
        self.searchButton.clicked.connect(self.searchPressed)
        self.resetButton = QPushButton("Reset")
        self.resetButton.clicked.connect(self.resetPressed)

        self.models = QListWidget()
        self.models.itemClicked.connect(self.modelClicked)

        self.specs = QTableWidget(1, 8)
        self.specs.setHorizontalHeaderLabels(
            ["Model", "Tension", "Length", "Pattern", "Skip M Holes",
             "Tie Off M", "Start C", "Tie Off C"])
        self.specs.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents)
        self.specs.verticalHeader().setVisible(False)

        self.models.addItems(self.brand.getListOfModels("", False))

        layout = QVBoxLayout()
        brandLayout = QHBoxLayout()
        brandLayout.addWidget(self.label)
        brandLayout.addWidget(self.dropdown)
        layout.addLayout(brandLayout)

        searchLayout = QHBoxLayout()
        searchLayout.addWidget(self.input)
        searchLayout.addWidget(self.searchButton)
        searchLayout.addWidget(self.resetButton)
        layout.addLayout(searchLayout)

        self.stackLayout = QStackedLayout()
        self.stackLayout.addWidget(self.models)
        self.stackLayout.addWidget(self.specs)
        layout.addLayout(self.stackLayout)

        layout.setContentsMargins(10, 5, 10, 10)
        layout.setSpacing(5)
        container = QWidget()
        container.setLayout(layout)

        # Set the central widget of the Window.
        self.setCentralWidget(container)

    # drop down picking brand handling
    def brandChanged(self, i):
        self.brand = self.dir.brands[i]
        self.stackLayout.setCurrentIndex(0)
        self.models.clear()
        self.models.addItems(self.brand.getListOfModels("", False))
    # handling search query

    def searchPressed(self):
        self.models.clear()
        input = self.input.text()
        self.models.addItems(self.brand.getListOfModels(input, False))
        self.stackLayout.setCurrentIndex(0)
        self.input.setText("")
        if input:
            self.input.setPlaceholderText(input)
        else:
            self.input.setPlaceholderText(PLACEHOLDER)

    def resetPressed(self):
        self.models.clear()
        self.models.addItems(self.brand.getListOfModels("", False))
        self.input.setText("")
        self.input.setPlaceholderText(PLACEHOLDER)

    def returnPressed(self):
        self.models.clear()
        input = self.input.text()
        self.models.addItems(self.brand.getListOfModels(input, False))
        self.stackLayout.setCurrentIndex(0)
        self.input.setText("")
        if input:
            self.input.setPlaceholderText(input)
        else:
            self.input.setPlaceholderText(PLACEHOLDER)

    # for selecting model to show specs for
    def modelClicked(self, item):
        self.stackLayout.setCurrentIndex(1)
        self.specs.setItem(0, 0, QTableWidgetItem(item.text()))
        for i in range(1, 8):
            self.specs.setItem(0, i, QTableWidgetItem(
                self.brand.getSpecs(item.text())[i-1]))


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
