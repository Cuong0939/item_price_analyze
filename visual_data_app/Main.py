import sys
from PySide6.QtWidgets import   (QApplication,QMainWindow,QWidget,QTableWidget,QHeaderView,
                                QHBoxLayout,QTableWidgetItem,QLineEdit,QPushButton,
                                QVBoxLayout,QLabel)
from PySide6.QtGui import QAction,QPainter
from PySide6.QtCore import Slot,Qt
from PySide6.QtCharts import QChartView,QPieSeries,QChart


class MainWindow(QMainWindow):
    # Init main window
    def __init__(self,widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("Tutorial")

        ## Make menu bar
        # Menu
        self.menu = self.menuBar()
        # Add element on menubar
        self.file_menu = self.menu.addMenu("File")
        self.help_menu = self.menu.addMenu("Help")

        # Exit QAction
        exit_action = QAction("Exit",self)
        exit_action.setShortcut("Ctrl+Q")


        ## First signal/slot connection
        exit_action.triggered.connect(self.app_exit)
        # Add exit option into file (parent element)
        self.file_menu.addAction(exit_action)

        # Set central widget for window
        self.setCentralWidget(widget)
    
    @Slot()
    def app_exit(self,checked):
        QApplication.quit()



# Empty widget and data
class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.items = 0

        # Example data
        self._data = {"Water": 24.5, "Electricity": 55.1, "Rent": 850.0,
                      "Supermarket": 230.4, "Internet": 29.99, "Bars": 21.85,
                      "Public transportation": 60.0, "Coffee": 22.45, "Restaurants": 120}

        # Make Left QTablWidget
        self.table = QTableWidget()
        # Set amout of table column
        self.table.setColumnCount(2)
        # Set header column labels
        self.table.setHorizontalHeaderLabels(["Description","Price"])
        # Grapable the columns
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


        ## Right side layout
        # Text area (edit)
        self.description = QLineEdit()
        self.price = QLineEdit()

        # Button for basic tasks
        self.add = QPushButton("Add")
        self.clear = QPushButton("Clear")
        self.quit = QPushButton("Quit")
        self.plot = QPushButton("PLot")

        # Set enable for add button
        self.add.setEnabled(False)

        ## Adding power for buttons

        # get the description and price from the fields,
        # insert a new empty row to the table,
        # set the values for the empty row in each column,
        # clear the input text fields,
        # include the global count of table rows.


        # Adding elements
        self.add.clicked.connect(self.add_element)
        
        # Quit application
        self.quit.clicked.connect(self.quit_app)

        # Clear whole table
        self.clear.clicked.connect(self.clear_table)

        # Plot chart on chart view
        self.plot.clicked.connect(self.plot_chart)

        # Fill example data
        self.fill_table()


        ## Verification step
        # Check invalid input for text area
        self.description.textChanged[str].connect(self.check_disable)
        self.price.textChanged[str].connect(self.check_disable)

        # Empty chart view
        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)


        # Define right layout and adding widgets
        self.right_layout = QVBoxLayout()
        self.right_layout.addWidget(QLabel("Description"))
        self.right_layout.addWidget(self.description)
        self.right_layout.addWidget(QLabel("Price"))
        self.right_layout.addWidget(self.price)
        self.right_layout.addWidget(self.add)
        self.right_layout.addWidget(self.plot)
        self.right_layout.addWidget(self.chart_view)
        self.right_layout.addWidget(self.clear)
        self.right_layout.addWidget(self.quit)

        #Make main layout
        self.layout = QHBoxLayout()

        #add QTableWidget into layout
        self.layout.addWidget(self.table)
        self.layout.addLayout(self.right_layout)

        # Set the layout to the widget
        self.setLayout(self.layout)





    # Fill example data
    def fill_table(self,data=None):
        data = self._data if not data else data
        for decs,price in data.items():
            # Take value from table by QTableWidgetItem
            DecsItem = QTableWidgetItem(decs)
            PriceItem = QTableWidgetItem(f"{price:.2f}")
            PriceItem.setTextAlignment(Qt.AlignRight)

            # Insert index for each row
            self.table.insertRow(self.items)
            # Insert 1st element for row on index
            self.table.setItem(self.items,0,DecsItem)
            # Insert 2nd element for row on index
            self.table.setItem(self.items,1,PriceItem)

            # Update index
            self.items+=1


    # Add Element fuction
    def add_element(self):
        # Take value from text area
        desc = self.description.text()
        price = self.price.text()

        # Insert value into table
        try:
            # Turning input value into QTableWidgetItem
            price_item = QTableWidgetItem(f"{float(price):.2f}")
            price_item.setTextAlignment(Qt.AlignRight)
            desc_item = QTableWidgetItem(desc)

            self.table.insertRow(self.items)
            self.table.setItem(self.items,0,desc_item)
            self.table.setItem(self.items,1,price_item)

            # Set text for text area after added
            self.description.setText("")
            self.price.setText("")

            # update index value
            self.items+=1
        except ValueError:
            print("Value Error",price)

    @Slot()
    def quit_app(self):
        QApplication.quit()


    @Slot()
    def clear_table(self):
        self.table.setRowCount(0)
        self.items = 0

    @Slot()
    def check_disable(self,input_value):
        if not self.description.text() or not self.price.text():
            self.add.setEnabled(False)
        else:
            self.add.setEnabled(True)


    @Slot()
    def plot_chart(self):
        # How to fill a QPieSeries
        # create a QPieSeries,
        # iterate over the table row IDs,
        # get the items at the i position,
        # add those values to the series.

        series = QPieSeries()

        # Get table information
        for i in range(self.table.rowCount()):
            text = self.table.item(i,0).text()
            number = float(self.table.item(i,1).text())
            series.append(text,number)
        
        # Create the Chart
        chart = QChart()
        # Add series into chart
        chart.addSeries(series)
        # Set legend for chart
        chart.legend().setAlignment(Qt.AlignLeft)
        # set chart for chart view
        self.chart_view.setChart(chart)


# Empty window
if __name__ =="__main__":
    app = QApplication(sys.argv)

    #set central widget
    widget = Widget()

    #set window argment
    window = MainWindow(widget)
    window.resize(800,600)
    window.show()




    #excute the app
    sys.exit(app.exec())