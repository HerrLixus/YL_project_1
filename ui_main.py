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
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.tab_2)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 791, 71))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.label_3.setText('Страна:')
        self.horizontalLayout.addWidget(self.label_3)
        self.country_box = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.country_box.setObjectName("country_box")
        self.horizontalLayout.addWidget(self.country_box)

        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.label.setText("Город:")
        self.horizontalLayout.addWidget(self.label)
        self.city_box = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.city_box.setObjectName("city_box")
        self.horizontalLayout.addWidget(self.city_box)

        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Улица:")
        self.horizontalLayout.addWidget(self.label_2)
        self.street_box = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.street_box.setObjectName("street_box")

        self.horizontalLayout.addWidget(self.street_box)
        self.tableWidget_2 = QtWidgets.QTableWidget(self.tab_2)
        self.tableWidget_2.setGeometry(QtCore.QRect(0, 70, 791, 381))
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
        self.listWidget.setGeometry(QtCore.QRect(0, 100, 791, 351))
        self.listWidget.setObjectName("listWidget")

        self.criteria_list = QtWidgets.QComboBox(self.tab)
        self.criteria_list.setGeometry(QtCore.QRect(10, 10, 141, 22))
        self.criteria_list.setObjectName("criteria_list")

        self.request_field = QtWidgets.QLineEdit(self.tab)
        self.request_field.setGeometry(QtCore.QRect(170, 10, 171, 20))
        self.request_field.setObjectName("request_field")

        self.tabWidget.insertTab(self.tabWidget.count() - 1, self.tab, "")
        self.tabWidget.setTabText(self.tabWidget.count() - 2, name)
        self.tabWidget.setCurrentIndex(self.tabWidget.count() - 2)
