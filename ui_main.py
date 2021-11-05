from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(815, 550)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 9, 800, 491))
        self.tabWidget.setObjectName("tabWidget")

        self.init_search_tab()

        self.new_theater_button = QtWidgets.QPushButton(MainWindow)
        self.new_theater_button.setGeometry(QtCore.QRect(10, 510, 150, 23))
        self.new_theater_button.setText('Добавить новый кинотеатр')

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 815, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.tabWidget.setCurrentIndex(1)


        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def init_search_tab(self):
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.tableWidget_2 = QtWidgets.QTableWidget(self.tab_2)
        self.tableWidget_2.setGeometry(QtCore.QRect(0, 10, 791, 440))
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabWidget.addTab(self.tab_2, "")
        self.tabWidget.setTabText(self.tabWidget.count() - 1, "+")

    def init_theater_tab_ui(self, name):
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")

        self.listWidget = QtWidgets.QListWidget(self.tab)
        self.listWidget.setGeometry(QtCore.QRect(0, 10, 791, 400))
        self.listWidget.setObjectName("listWidget")

        self.add_session_button = QtWidgets.QPushButton(self.tab)
        self.add_session_button.setGeometry(QtCore.QRect(5, 420, 100, 25))
        self.add_session_button.setText('Добавить сеанс')

        self.tabWidget.insertTab(self.tabWidget.count() - 1, self.tab, "")
        self.tabWidget.setTabText(self.tabWidget.count() - 2, name)
        self.tabWidget.setCurrentIndex(self.tabWidget.count() - 2)
        return self.tab
