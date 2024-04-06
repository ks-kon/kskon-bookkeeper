"""
модуль для взаимодействия sql таблицы расходов с интерфейсом
"""
import datetime

from .database import DatabaseConnection
from .memory_repository import MemoryRepository
from ..models.category import Category


class Connector:
    """
    класс для взаимодействия sql таблицы расходов с интерфейсом
    параметр db - датабаза из класса DatabaseConnection
    max_id - id
    """
    def __init__(self, db: DatabaseConnection, mem_repo: MemoryRepository):
        self.db = db
        self.max_id = int(self.db.execute_query('SELECT MAX(exp_id) FROM Expenses')[0][0])
        self.mem_repo = mem_repo

    def changed_expense(self, column: int, exp_id: str, exp_data: str) -> None:
        """
        изменение расхода
        """
        if column == 1:
            data = exp_data
            query = '''UPDATE Expenses SET date = ? WHERE exp_id = ?'''
        elif column == 2:
            data = float(exp_data)
            query = '''UPDATE Expenses SET sum = ? WHERE exp_id = ?'''
        elif column == 3:
            data = exp_data
            query = '''UPDATE Expenses SET cat = ? WHERE exp_id = ?'''
        elif column == 4:
            data = exp_data
            query = '''UPDATE Expenses SET comm = ? WHERE exp_id = ?'''
        if column in [1, 2, 3, 4]:
            params = (data, int(exp_id))
            self.db.execute_query(query, params)

    def add_expense(self, summa: str, cat: str, comm: str) -> None:
        """
        добавление нового расхода
        """
        query = 'INSERT INTO Expenses(exp_id, date, sum, cat, comm) VALUES (?,?,?,?,?)'
        new_id = self.max_id + 1
        self.max_id += 1
        date = datetime.date.today().strftime('%Y-%m-%d')
        params = (new_id, date, float(summa), cat, comm)
        self.db.execute_query(query, params)

    def send_categories_to_db(self):
        cat_tree = Category.make_tree_from_repo(Category, self.mem_repo)
        query0 = 'DELETE FROM Categories'
        self.db.execute_query(query0)
        query = 'INSERT INTO Categories(name, parent) VALUES (?,?)'
        for val in cat_tree:
            self.db.execute_query(query, params=val)
