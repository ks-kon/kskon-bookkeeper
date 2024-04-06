"""
main
"""
import sys
from PySide6.QtWidgets import QApplication

from bookkeeper.repository.database import DatabaseConnection
from bookkeeper.repository.memory_repository import MemoryRepository
# from bookkeeper.repository.abstract_repository import AbstractRepository


from bookkeeper.models.category import Category

from bookkeeper.repository.connector import Connector

from bookkeeper.models.budget import Budget

from bookkeeper.view.view import MainWindow



if __name__ == '__main__':
    db = DatabaseConnection()
    cat_mem_repo = MemoryRepository[Category]()
    cat_tree = db.execute_query('SELECT * FROM Categories')
    Category.create_from_tree(tree=cat_tree, repo=cat_mem_repo)
    conn = Connector(db, cat_mem_repo)
    budg = Budget(db, 1000, 5000, 100000)

    app = QApplication(sys.argv)
    main_window = MainWindow(db, conn, budg, cat_mem_repo)
    main_window.show()

    app.exec()
