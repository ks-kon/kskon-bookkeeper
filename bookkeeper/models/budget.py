"""
Взаимодействие доступного бюджета с интерфейсом
"""
import datetime

from bookkeeper.bookkeeper.repository.database import DatabaseConnection


class Budget:
    """
    Взаимодействие доступного бюджета с интерфейсом
    """
    def __init__(self, db: DatabaseConnection,
                 day_budget: float, week_budget: float, month_budget: float):
        self.db = db
        self.today = datetime.date.today()
        self.day_budget = day_budget
        self.week_budget = week_budget
        self.month_budget = month_budget

    def day_sum(self) -> float:
        """
        сумма расходов за текущий день
        """
        query = 'SELECT SUM(sum) FROM Expenses WHERE date = ?'
        return self.db.execute_query(query,
                                     params=(self.today.strftime('%Y-%m-%d'),))[0][0]

    def week_sum(self) -> float:
        """
        сумма расходов за текущую неделю
        """
        query = 'SELECT SUM(sum) FROM Expenses WHERE strftime("%w", date) = ?'
        return self.db.execute_query(query, params=(self.today.strftime("%w"),))[0][0]

    def month_sum(self) -> float:
        """
        сумма расходов за текущий месяц
        """
        query = "SELECT SUM(sum) FROM Expenses WHERE strftime('%m',date) = ?"
        return self.db.execute_query(query, params=(self.today.strftime('%m'),))[0][0]

    def create_budget_table(self) -> list:
        """
        таблица для представления бюджета
        """
        table = [[self.day_sum(), self.day_budget],
                 [self.week_sum(), self.week_budget],
                 [self.month_sum(), self.month_budget]]
        return table

    def changed_budget(self, row: int, column: int, data: str):
        """
        изменить доступный бюджет на день, неделю, месяц
        """
        if column == 2:
            if row == 0:
                self.day_budget = data
            elif row == 1:
                self.week_budget = data
            elif row == 2:
                self.month_budget = data
