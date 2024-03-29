"""
интерфейс
"""

from PySide6.QtWidgets import (QWidget, QLabel, QVBoxLayout,
                               QPushButton, QTableWidget, QHeaderView,
                               QLineEdit, QComboBox, QHBoxLayout, QGroupBox)
from PySide6 import QtWidgets

from bookkeeper.repository.database import DatabaseConnection
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.view.connector import Connector
from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category


class MainWindow(QWidget):
    """
    класс интерфейс
    """
    def __init__(self, db: DatabaseConnection,
                 connector: Connector, budget: Budget, repo: MemoryRepository[Category]):
        super().__init__()

        self.db = db
        self.connector = connector
        self.budget = budget
        self.repo = repo

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
        self.b_label = QLabel('Бюджет - суммарные траты')
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
        self.budg_set_data(budget.create_budget_table())
        self.budget_table.cellChanged.connect(self.budg_on_cell_changed)
        self.layout.addWidget(self.budget_table)

        # для добавления нового расхода
        self.h_layout = QHBoxLayout(self)
        self.line_label = QLabel('Добавить новый расход: сумма, категория, комментарий')
        self.layout.addWidget(self.line_label)
        self.lineedit = QLineEdit()
        self.layout.addWidget(self.lineedit)

        self._horizontal_group_box = QGroupBox()
        self.h_layout = QHBoxLayout()
        self.sum_edit = QLineEdit('Сумма')
        self.cat_edit = QComboBox()
        self.cat_edit.addItems([cat.name for cat in repo.get_all()])
        self.comm_edit = QLineEdit('Комментарий')
        self.h_layout.addWidget(self.sum_edit)
        self.h_layout.addWidget(self.cat_edit)
        self.h_layout.addWidget(self.comm_edit)
        self._horizontal_group_box.setLayout(self.h_layout)
        self.layout.addWidget(self._horizontal_group_box)

        self.exp_button = QPushButton('Добавить новый расход')
        self.exp_button.clicked.connect(self.on_exp_button_clicked)
        self.layout.addWidget(self.exp_button)

        # для просмотра и редактирования списка категорий
        self.cat_label = QLabel('Добавить категорию')
        self.layout.addWidget(self.cat_label)

        # self.combobox = QComboBox()
        self.select_parent_label = QLabel('Выберите родителя')
        self.parent_combobox = QComboBox()
        self.parent_combobox.addItems(['Нет родителя'])
        self.parent_combobox.addItems(
            [cat.name+', '+str(cat.pk) for cat in repo.get_all()])
        self.new_cat_name_lineedit = QLineEdit('Введите название новой категории')
        self.cat_add_button = QPushButton('Добавить новую категорию')
        self.cat_add_button.clicked.connect(self.on_cat_add_button_clicked)

        self.layout.addWidget(self.parent_combobox)
        self.layout.addWidget(self.new_cat_name_lineedit)
        self.layout.addWidget(self.cat_add_button)

        # Устанавливаем макет для главного окна
        self.setLayout(self.layout)

        # Устанавливаем параметры главного окна
        self.setWindowTitle('Bookkeeper')
        self.setGeometry(200, 200, 800, 400)

        with open('view/style.qss', 'r') as f:
            self.setStyleSheet(f.read())

    def exp_set_data(self, data: list[list[str]]) -> None:
        """
        заполняет таблицу расходов
        """
        for i, row in enumerate(data):
            for j, x in enumerate(row):
                self.expenses_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(x)))

    def budg_set_data(self, data: list[list[str]]) -> None:
        """
        заполняет таблицу с бюджетом на неделю
        """
        for i, row in enumerate(data):
            for j, x in enumerate(row):
                self.budget_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(x)))

    def exp_on_cell_changed(self, row: int, column: int) -> None:
        """
        отсылает измененные данные расхода в Connector
        """
        changed_expense_id = self.expenses_table.item(row, 0).text()
        changed_data = self.expenses_table.item(row, column).text()
        self.connector.changed_expense(row, column, changed_expense_id, changed_data)

    def budg_on_cell_changed(self, row: int, column: int) -> None:
        """
        отсылает измененные данные бюджета в Budget
        """
        changed_budget = self.budget_table.item(row, column).text()
        self.budget.changed_budget(row, column, changed_budget)

    def on_exp_button_clicked(self) -> None:
        """
        отсылает новый расход в Connector
        """
        self.connector.add_expense(self.sum_edit.text(),
                                   self.cat_edit.currentText(), self.comm_edit.text())
        self.exp_set_data(self.db.execute_query('SELECT * FROM Expenses'))

    def on_cat_add_button_clicked(self) -> None:
        """
        добавляет категорию
        """
        new_cat_name = self.new_cat_name_lineedit.text()
        if self.parent_combobox.currentText() == 'Нет родителя':
            new_cat = Category(name=new_cat_name)
        else:
            new_cat_parent_id = int(self.parent_combobox.currentText().split(', ')[1])
            new_cat = Category(name=new_cat_name, parent=new_cat_parent_id)
        self.repo.add(new_cat)
