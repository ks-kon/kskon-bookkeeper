# import sys
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QTableWidget, QHeaderView,
                               QLineEdit, QComboBox)
from PySide6 import QtWidgets


class MainWindow(QWidget):
    def __init__(self, db, connector):
        super().__init__()

        self.db = db
        self.connector = connector

        # Создаем главный макет
        self.layout = QVBoxLayout(self)

        # Создаем виджеты

        # для отображения списка расходов с возможностью редактирования
        self.e_label = QLabel('Список расходов')
        self.layout.addWidget(self.e_label)

        self.expenses_table = QTableWidget(5, 20)
        self.expenses_table.setColumnCount(5)
        self.expenses_table.setRowCount(20)
        self.expenses_table.setHorizontalHeaderLabels(
            "Id Дата Сумма Категория Комментарий".split())
        header = self.expenses_table.horizontalHeader()
        header.setSectionResizeMode(
            0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(
            1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(
            2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(
            3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(
            4, QHeaderView.Stretch)
        self.expenses_table.verticalHeader().hide()
        self.exp_set_data(self.db.execute_query('SELECT * FROM Expenses'))
        self.expenses_table.cellChanged.connect(self.exp_on_cell_changed)
        self.layout.addWidget(self.expenses_table)

        # для отображения бюджета на день/неделю/месяц с возможностью редактирования
        self.b_label = QLabel('Бюджет')
        self.layout.addWidget(self.b_label)

        self.budget_table = QTableWidget(2, 3)
        self.budget_table.setColumnCount(2)
        self.budget_table.setRowCount(3)
        self.budget_table.setHorizontalHeaderLabels(
            "Сумма Бюджет".split())
        self.budget_table.setVerticalHeaderLabels('День Неделя Месяц'.split())
        b_header = self.budget_table.horizontalHeader()
        b_header.setSectionResizeMode(
            0, QHeaderView.ResizeToContents)
        b_header.setSectionResizeMode(
            1, QHeaderView.Stretch)
        self.budg_set_data([['skdjjfk', '55']])
        self.budget_table.cellChanged.connect(self.budg_on_cell_changed)
        self.layout.addWidget(self.budget_table)

        # для добавления нового расхода
        self.line_label = QLabel('Добавить новый расход: сумма, категория, комментарий')
        self.layout.addWidget(self.line_label)
        self.lineedit = QLineEdit()
        self.layout.addWidget(self.lineedit)

        self.exp_button = QPushButton('Добавить новый расход')
        self.exp_button.clicked.connect(self.on_exp_button_clicked)
        self.layout.addWidget(self.exp_button)

        # для просмотра и редактирования списка категорий
        self.cat_label = QLabel('Категории')
        self.layout.addWidget(self.cat_label)

        self.combobox = QComboBox()
        self.combobox.addItems(["One", "Two", "Three"])
        self.combobox.setEditable(True)
        # self.combobox.currentIndexChanged.connect(self.on_combobox_changed)
        # self.combobox.ValueChanged.connect(self.on_combobox_changed)
        self.layout.addWidget(self.combobox)

        # Устанавливаем макет для главного окна
        self.setLayout(self.layout)

        # Устанавливаем параметры главного окна
        self.setWindowTitle('Bookkeeper')
        self.setGeometry(200, 200, 800, 400)


    def exp_set_data(self, data):
        for i, row in enumerate(data):
            for j, x in enumerate(row):
                self.expenses_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(x)))

    def budg_set_data(self, data):
        for i, row in enumerate(data):
            for j, x in enumerate(row):
                self.budget_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(x)))

    def exp_on_cell_changed(self, row, column):
        changed_expense_id = self.expenses_table.item(row, 0).text()
        changed_data = self.expenses_table.item(row, column).text()
        self.connector.changed_expense(row, column, changed_expense_id, changed_data)

    def budg_on_cell_changed(self, row, column):
        changed_budget = self.budget_table.item(row, column).text()

    def on_exp_button_clicked(self):
        new_expense = self.lineedit.text().split(' ')
        self.connector.add_expense(new_expense)
        self.exp_set_data(self.db.execute_query('SELECT * FROM Expenses'))

    def on_combobox_changed(self, value):
        new_category = value
        print(new_category)